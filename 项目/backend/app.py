from __future__ import annotations

import base64
import os
import uuid
import logging
from typing import Any, Dict, List, Optional, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from utils.ai_service import create_ai_service
except Exception as exc:  # pragma: no cover - import guard for broken env
    create_ai_service = None
    AI_IMPORT_ERROR = str(exc)
else:
    AI_IMPORT_ERROR = None

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("guidebot")

_ai_service = None


def _parse_bool(value: Optional[str], default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


ALLOW_MOCK_ON_AI_ERROR = _parse_bool(os.getenv("AI_ALLOW_MOCK_FALLBACK"), True)


def _get_ai_service() -> Tuple[Optional[Any], Optional[str]]:
    global _ai_service

    if _ai_service is not None:
        return _ai_service, None

    if create_ai_service is None:
        return None, f"AI service import failed: {AI_IMPORT_ERROR}"

    try:
        _ai_service = create_ai_service()
        return _ai_service, None
    except Exception as exc:  # pragma: no cover - startup guard
        logger.exception("Failed to initialize AI service")
        return None, str(exc)


def _save_base64_image(base64_str: str, filename: str) -> Optional[str]:
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",", 1)[1]

        image_data = base64.b64decode(base64_str)
        path = os.path.join(UPLOAD_FOLDER, filename)

        with open(path, "wb") as f:
            f.write(image_data)

        return path
    except Exception:
        logger.exception("Failed to decode/save uploaded image")
        return None


def _build_image_data_url(filepath: str) -> str:
    with open(filepath, "rb") as f:
        raw = f.read()
    return f"data:image/png;base64,{base64.b64encode(raw).decode('utf-8')}"


def _default_steps() -> List[Dict[str, Any]]:
    return [
        {
            "step": 1,
            "description": "点击页面右上角的“登录”按钮，进入登录流程。",
            "rect": {"x": 650, "y": 50, "width": 100, "height": 40},
            "color": "#ff0000",
        },
        {
            "step": 2,
            "description": "在用户名输入框中填写你的账号信息。",
            "rect": {"x": 300, "y": 200, "width": 200, "height": 40},
            "color": "#00aa00",
        },
        {
            "step": 3,
            "description": "在密码输入框中输入密码，并确认输入无误。",
            "rect": {"x": 300, "y": 260, "width": 200, "height": 40},
            "color": "#0000ff",
        },
        {
            "step": 4,
            "description": "点击“确认登录”按钮，等待页面跳转完成。",
            "rect": {"x": 350, "y": 350, "width": 120, "height": 45},
            "color": "#ff8800",
        },
    ]


@app.route("/api/health", methods=["GET"])
def health_check():
    service, ai_error = _get_ai_service()
    ai_ready = service is not None and not ai_error

    return jsonify(
        {
            "status": "healthy",
            "service": "GuideBot Backend",
            "version": "1.1.0",
            "ai": {
                "ready": ai_ready,
                "allow_mock_fallback": ALLOW_MOCK_ON_AI_ERROR,
                "error": ai_error,
            },
            "endpoints": [
                "/api/health",
                "/api/process/image",
                "/api/process/url",
                "/api/process/text",
                "/api/community/guides",
                "/api/community/share",
                "/api/test/ai",
            ],
        }
    )


@app.route("/api/process/image", methods=["POST"])
def process_image():
    filepath: Optional[str] = None

    try:
        data = request.get_json(silent=True) or {}
        image_base64 = data.get("image")

        if not image_base64:
            return jsonify({"success": False, "error": "缺少图片 Base64 数据。"}), 400

        filename = f"{uuid.uuid4().hex}.png"
        filepath = _save_base64_image(image_base64, filename)

        if not filepath:
            return jsonify({"success": False, "error": "保存图片失败。"}), 500

        service, ai_error = _get_ai_service()
        if service is None:
            logger.error("AI service unavailable: %s", ai_error)
            if not ALLOW_MOCK_ON_AI_ERROR:
                return jsonify({"success": False, "error": f"AI service unavailable: {ai_error}"}), 503

            return jsonify(
                {
                    "success": True,
                    "steps": _default_steps(),
                    "title": "操作引导（回退）",
                    "summary": "AI 服务暂不可用，以下为示例引导步骤。",
                    "estimated_time": "约3分钟",
                    "difficulty": "初级",
                    "prerequisites": ["确认网络连接稳定。", "准备好账号与必要权限。"],
                    "common_mistakes": ["漏点关键按钮。", "提交前未检查输入信息。"],
                    "final_check": ["页面跳转成功。", "操作结果已生效。"],
                    "image": _build_image_data_url(filepath),
                    "message": "AI 服务不可用，已返回回退说明。",
                    "ai_used": False,
                    "source": "mock",
                    "error": ai_error,
                }
            )

        ai_result = service.analyze_image(filepath)
        steps = ai_result.get("steps") or []
        title = ai_result.get("title") or "操作引导"
        summary = ai_result.get("summary") or "请按以下步骤依次完成操作。"
        estimated_time = ai_result.get("estimated_time") or "约3分钟"
        difficulty = ai_result.get("difficulty") or "初级"
        prerequisites = ai_result.get("prerequisites") or []
        common_mistakes = ai_result.get("common_mistakes") or []
        final_check = ai_result.get("final_check") or []
        ai_used = bool(ai_result.get("ai_used"))
        source = "ai" if ai_used else "mock"

        if not ai_result.get("success"):
            logger.error("AI analyze_image failed: %s", ai_result.get("error"))
            status_code = 502 if not ALLOW_MOCK_ON_AI_ERROR else 200
            return jsonify(
                {
                    "success": ALLOW_MOCK_ON_AI_ERROR,
                    "steps": steps if ALLOW_MOCK_ON_AI_ERROR else [],
                    "title": title,
                    "summary": summary,
                    "estimated_time": estimated_time,
                    "difficulty": difficulty,
                    "prerequisites": prerequisites,
                    "common_mistakes": common_mistakes,
                    "final_check": final_check,
                    "image": _build_image_data_url(filepath),
                    "message": "AI 调用失败。" if not ALLOW_MOCK_ON_AI_ERROR else "AI 生成失败，已返回回退说明。",
                    "ai_used": False,
                    "source": "mock" if ALLOW_MOCK_ON_AI_ERROR else "error",
                    "error": ai_result.get("error"),
                }
            ), status_code

        if not steps:
            logger.warning("AI returned success but no steps.")
            if ALLOW_MOCK_ON_AI_ERROR:
                steps = _default_steps()
                title = "操作引导（回退）"
                summary = "AI 未返回有效步骤，已切换为回退说明。"
                estimated_time = "约3分钟"
                difficulty = "初级"
                prerequisites = ["确认网络连接稳定。", "准备好账号与必要权限。"]
                common_mistakes = ["漏点关键按钮。", "提交前未检查输入信息。"]
                final_check = ["页面跳转成功。", "操作结果已生效。"]
                ai_used = False
                source = "mock"

        return jsonify(
            {
                "success": True,
                "steps": steps,
                "title": title,
                "summary": summary,
                "estimated_time": estimated_time,
                "difficulty": difficulty,
                "prerequisites": prerequisites,
                "common_mistakes": common_mistakes,
                "final_check": final_check,
                "image": _build_image_data_url(filepath),
                "message": "图片分析完成。",
                "ai_used": ai_used,
                "source": source,
                "error": ai_result.get("error"),
            }
        )

    except Exception as exc:  # pragma: no cover - last-line guard
        logger.exception("Unexpected error in /api/process/image")
        return jsonify({"success": False, "error": f"服务端内部错误: {exc}"}), 500
    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                logger.exception("Failed to cleanup temp image: %s", filepath)


@app.route("/api/process/url", methods=["POST"])
def process_url():
    try:
        data = request.get_json(silent=True) or {}
        url = (data.get("url") or "").strip()

        if not url:
            return jsonify({"success": False, "error": "缺少网址参数。"}), 400

        steps = [
            {
                "step": 1,
                "description": f"先打开网址：{url[:50]}",
                "rect": {"x": 100, "y": 100, "width": 300, "height": 50},
                "color": "#ff0000",
            },
            {
                "step": 2,
                "description": "等待页面元素加载完成，再开始下一步操作。",
                "rect": {"x": 150, "y": 200, "width": 250, "height": 40},
                "color": "#00aa00",
            },
            {
                "step": 3,
                "description": "根据页面导航找到目标功能入口并点击进入。",
                "rect": {"x": 200, "y": 300, "width": 200, "height": 60},
                "color": "#0000ff",
            },
        ]

        return jsonify(
            {
                "success": True,
                "steps": steps,
                "title": "网址操作引导",
                "summary": "以下是根据网址生成的示例步骤。",
                "estimated_time": "约3分钟",
                "difficulty": "初级",
                "prerequisites": ["确认网址可正常访问。", "等待页面加载完成后再操作。"],
                "common_mistakes": ["页面未加载完成就开始点击，导致操作失败。"],
                "final_check": ["已进入目标功能页面。"],
                "url": url,
                "message": "网址处理完成（示例数据）。",
            }
        )

    except Exception as exc:
        logger.exception("Error in /api/process/url")
        return jsonify({"success": False, "error": f"处理网址失败: {exc}"}), 500


@app.route("/api/process/text", methods=["POST"])
def process_text():
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()

        if not text:
            return jsonify({"success": False, "error": "缺少文本描述。"}), 400

        steps = [
            {
                "step": 1,
                "description": "打开与你目标任务相关的应用或网页。",
                "rect": {"x": 100, "y": 100, "width": 100, "height": 50},
                "color": "#ff6600",
            },
            {
                "step": 2,
                "description": "定位目标入口按钮，确认页面状态后点击。",
                "rect": {"x": 200, "y": 200, "width": 100, "height": 30},
                "color": "#ff6600",
            },
            {
                "step": 3,
                "description": "根据系统提示完成信息填写并提交操作。",
                "rect": {"x": 150, "y": 300, "width": 150, "height": 40},
                "color": "#ff6600",
            },
        ]

        return jsonify(
            {
                "success": True,
                "steps": steps,
                "title": "文本任务引导",
                "summary": "以下是根据文本描述生成的示例步骤。",
                "estimated_time": "约3分钟",
                "difficulty": "初级",
                "prerequisites": ["确认你有相关应用或网页的访问权限。"],
                "common_mistakes": ["跳过确认步骤，导致结果不完整。"],
                "final_check": ["目标任务已按描述完成。"],
                "text": text,
                "scenario": "general",
                "message": "文本处理完成（示例数据）。",
            }
        )

    except Exception as exc:
        logger.exception("Error in /api/process/text")
        return jsonify({"success": False, "error": f"处理文本失败: {exc}"}), 500


@app.route("/api/community/guides", methods=["GET"])
def get_community_guides():
    guides = [
        {
            "id": 1,
            "title": "WeChat Moments Quick Guide",
            "author": "UserA",
            "likes": 42,
            "steps": 3,
            "created_at": "2026-01-15",
            "scenario": "social",
        },
        {
            "id": 2,
            "title": "Course Selection Steps",
            "author": "UserB",
            "likes": 28,
            "steps": 4,
            "created_at": "2026-01-20",
            "scenario": "education",
        },
    ]

    return jsonify(
        {
            "success": True,
            "guides": guides,
            "total": len(guides),
            "message": "Community guides.",
        }
    )


@app.route("/api/community/share", methods=["POST"])
def share_to_community():
    try:
        data = request.get_json(silent=True) or {}
        if "title" not in data or "steps" not in data:
            return jsonify({"success": False, "error": "Missing title or steps."}), 400

        return jsonify(
            {
                "success": True,
                "message": "Shared successfully.",
                "share_id": uuid.uuid4().hex,
            }
        )

    except Exception as exc:
        logger.exception("Error in /api/community/share")
        return jsonify({"success": False, "error": f"Share failed: {exc}"}), 500


@app.route("/api/test/ai", methods=["GET"])
def test_ai_connection():
    service, ai_error = _get_ai_service()
    if service is None:
        return jsonify(
            {
                "success": False,
                "status": "unavailable",
                "message": f"AI service unavailable: {ai_error}",
            }
        ), 503

    result = service.test_connection()
    status_code = 200 if result.get("success") else 503
    return jsonify(result), status_code


@app.route("/api/info", methods=["GET"])
def api_info():
    return jsonify(
        {
            "name": "GuideBot API",
            "description": "Guide generation backend API",
            "version": "1.1.0",
            "endpoints": {
                "GET": [
                    "/api/health",
                    "/api/community/guides",
                    "/api/test/ai",
                    "/api/info",
                ],
                "POST": [
                    "/api/process/image",
                    "/api/process/url",
                    "/api/process/text",
                    "/api/community/share",
                ],
            },
        }
    )


if __name__ == "__main__":
    logger.info("Starting GuideBot backend on http://localhost:5000")
    app.run(debug=False, port=5000, host="0.0.0.0", use_reloader=False)
