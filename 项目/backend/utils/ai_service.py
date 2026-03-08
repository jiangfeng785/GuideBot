from __future__ import annotations

import base64
import json
import os
import re
import time
from typing import Any, Dict, List, Optional

import requests


def _load_env_if_available() -> None:
    """Load .env if python-dotenv exists; skip silently otherwise."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return

    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)


class QwenVLService:
    def __init__(self, api_key: Optional[str] = None):
        _load_env_if_available()

        self.api_key = (api_key or os.getenv("DASHSCOPE_API_KEY") or "").strip()
        self.base_url = (
            os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
        )
        self.model = os.getenv("DASHSCOPE_MODEL", "qwen-max")
        self.allow_mock_fallback = self._parse_bool(os.getenv("AI_ALLOW_MOCK_FALLBACK"), True)
        self.request_timeout_seconds = self._parse_int(os.getenv("AI_REQUEST_TIMEOUT_SECONDS"), 90)
        self.request_retries = self._parse_int(os.getenv("AI_REQUEST_RETRIES"), 1)
        self.retry_backoff_seconds = self._parse_float(os.getenv("AI_REQUEST_RETRY_BACKOFF_SECONDS"), 1.5)
        self.image_max_tokens = self._parse_int(os.getenv("AI_IMAGE_MAX_TOKENS"), 1800)
        self.text_max_tokens = self._parse_int(os.getenv("AI_TEXT_MAX_TOKENS"), 1300)
        self.url_max_tokens = self._parse_int(os.getenv("AI_URL_MAX_TOKENS"), 1300)

    @staticmethod
    def _parse_bool(value: Optional[str], default: bool = True) -> bool:
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _parse_int(value: Optional[str], default: int) -> int:
        if value is None:
            return default
        try:
            parsed = int(value.strip())
            return parsed if parsed >= 0 else default
        except Exception:
            return default

    @staticmethod
    def _parse_float(value: Optional[str], default: float) -> float:
        if value is None:
            return default
        try:
            parsed = float(value.strip())
            return parsed if parsed >= 0 else default
        except Exception:
            return default

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _system_prompt(self) -> str:
        return (
            "你是资深中文产品导师与信息架构师。"
            "你的任务是产出可执行、细节充分、表达优雅的中文操作引导。"
            "文风固定为亲和版：语气友好、解释耐心、对新手友善，但避免啰嗦。"
            "必须坚持：步骤清晰、动作明确、预期可验证、语言自然。"
        )

    def _guide_json_schema(self) -> str:
        return (
            "{"
            "\"title\":\"简洁标题\","
            "\"summary\":\"2-3句总览，说明目标、适用人群与完成收益\","
            "\"estimated_time\":\"如 约8分钟\","
            "\"difficulty\":\"初级/中级/高级\","
            "\"prerequisites\":[\"前置条件1\",\"前置条件2\"],"
            "\"steps\":["
            "{"
            "\"step\":1,"
            "\"title\":\"步骤小标题\","
            "\"description\":\"45-90字，写清点击位置/输入内容/操作顺序\","
            "\"purpose\":\"说明这一步为什么必要\","
            "\"expected_result\":\"完成后应该看到的具体界面变化\","
            "\"tip\":\"可选，效率技巧\","
            "\"warning\":\"可选，风险提醒\","
            "\"rect\":{\"x\":0,\"y\":0,\"width\":120,\"height\":40},"
            "\"color\":\"#ff0000\""
            "}"
            "],"
            "\"common_mistakes\":[\"常见错误1\",\"常见错误2\"],"
            "\"final_check\":[\"完成检查点1\",\"完成检查点2\"]"
            "}"
        )

    def _build_guide_prompt(self, source_type: str, source_text: Optional[str] = None) -> str:
        context = ""
        if source_type == "image":
            context = "输入是截图，请结合可见UI元素推断操作流程。"
        elif source_type == "url":
            context = f"输入是网址：{source_text or ''}。请给出通用网页操作引导，并明确页面加载、导航定位、提交确认。"
        elif source_type == "text":
            context = f"输入是任务描述：{source_text or ''}。请围绕该目标生成完整执行方案。"

        return (
            f"{context}"
            "只允许输出 JSON，不得输出任何额外说明、前后缀、Markdown。"
            f"JSON字段必须严格为：{self._guide_json_schema()}"
            "质量要求："
            "1) 全部使用简体中文，避免英文夹杂。"
            "2) 步骤数量为 4-6 步。"
            "3) 每步 description 要包含“动作 + 位置/对象 + 判定标准”，且为完整句。"
            "4) 每步必须提供 purpose 与 expected_result，tip/warning 至少二者其一。"
            "5) 使用亲和版表达：像在手把手指导同学，语气温和、清楚、有陪伴感。"
            "6) 文案风格专业但不生硬，避免口号式空话，如“按提示操作即可”。"
            "7) summary、common_mistakes、final_check 必须具体，不能泛泛而谈。"
            "8) 若信息不充分，基于常见产品交互做合理假设，并在描述中给出保守操作路径。"
        )

    def _request_chat_completion(self, messages: List[Dict[str, Any]], max_tokens: int = 1800) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.45,
            "top_p": 0.9,
            "max_tokens": max_tokens,
        }
        attempts = self.request_retries + 1
        last_error = "AI 请求失败"
        for idx in range(attempts):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.request_timeout_seconds,
                )
                if response.status_code != 200:
                    last_error = f"AI API error {response.status_code}: {response.text[:300]}"
                    # 5xx 或 429 才重试；4xx 参数错误不重试
                    should_retry_status = response.status_code >= 500 or response.status_code == 429
                    if idx < attempts - 1 and should_retry_status:
                        time.sleep(self.retry_backoff_seconds * (idx + 1))
                        continue
                    return {"success": False, "error": last_error}

                result = response.json()
                content = self._extract_content(result)
                if content is None:
                    return {
                        "success": False,
                        "error": "AI 响应缺少必要字段（choices/message/content）",
                        "raw_response": json.dumps(result, ensure_ascii=False)[:1000],
                    }
                return {"success": True, "content": content}
            except requests.RequestException as exc:
                last_error = f"AI 请求失败: {exc}"
                if idx < attempts - 1:
                    time.sleep(self.retry_backoff_seconds * (idx + 1))
                    continue
                return {"success": False, "error": last_error}

        return {"success": False, "error": last_error}

    def _guide_from_content(self, content: Any) -> Dict[str, Any]:
        guide = self._parse_ai_response(content)
        steps = guide.get("steps", [])
        if not steps:
            return {
                "success": False,
                "steps": [],
                "error": "无法从 AI 响应中解析出有效步骤",
                "raw_response": str(content)[:1000],
            }
        return {
            "success": True,
            "steps": steps,
            "title": guide.get("title"),
            "summary": guide.get("summary"),
            "estimated_time": guide.get("estimated_time"),
            "difficulty": guide.get("difficulty"),
            "prerequisites": guide.get("prerequisites"),
            "common_mistakes": guide.get("common_mistakes"),
            "final_check": guide.get("final_check"),
            "ai_used": True,
            "source": "ai",
            "error": None,
        }

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        if not os.path.exists(image_path):
            return self._error_or_mock(f"图片文件不存在: {image_path}")

        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")

        try:
            image_base64 = self.encode_image_to_base64(image_path)
            prompt = self._build_guide_prompt(source_type="image")
            req = self._request_chat_completion(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                            },
                            {"type": "text", "text": prompt},
                        ],
                    },
                ],
                max_tokens=self.image_max_tokens,
            )
            if not req.get("success"):
                return self._error_or_mock(req.get("error", "AI 请求失败"), req.get("raw_response"))
            parsed = self._guide_from_content(req.get("content"))
            if not parsed.get("success"):
                return self._error_or_mock(parsed.get("error", "AI 解析失败"), parsed.get("raw_response"))
            return parsed

        except requests.RequestException as exc:
            return self._error_or_mock(f"AI 请求失败: {exc}")
        except Exception as exc:
            return self._error_or_mock(f"AI 分析异常: {exc}")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        text = (text or "").strip()
        if not text:
            return self._error_or_mock("文本为空，无法生成引导")
        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")

        try:
            prompt = self._build_guide_prompt(source_type="text", source_text=text)
            req = self._request_chat_completion(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.text_max_tokens,
            )
            if not req.get("success"):
                return self._error_or_mock(req.get("error", "AI 请求失败"), req.get("raw_response"))
            parsed = self._guide_from_content(req.get("content"))
            if not parsed.get("success"):
                return self._error_or_mock(parsed.get("error", "AI 解析失败"), parsed.get("raw_response"))
            return parsed
        except requests.RequestException as exc:
            return self._error_or_mock(f"AI 请求失败: {exc}")
        except Exception as exc:
            return self._error_or_mock(f"AI 分析异常: {exc}")

    def analyze_url(self, url: str) -> Dict[str, Any]:
        url = (url or "").strip()
        if not url:
            return self._error_or_mock("网址为空，无法生成引导")
        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")

        try:
            prompt = self._build_guide_prompt(source_type="url", source_text=url)
            req = self._request_chat_completion(
                messages=[
                    {"role": "system", "content": self._system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.url_max_tokens,
            )
            if not req.get("success"):
                return self._error_or_mock(req.get("error", "AI 请求失败"), req.get("raw_response"))
            parsed = self._guide_from_content(req.get("content"))
            if not parsed.get("success"):
                return self._error_or_mock(parsed.get("error", "AI 解析失败"), parsed.get("raw_response"))
            return parsed
        except requests.RequestException as exc:
            return self._error_or_mock(f"AI 请求失败: {exc}")
        except Exception as exc:
            return self._error_or_mock(f"AI 分析异常: {exc}")

    def _extract_content(self, result: Dict[str, Any]) -> Optional[Any]:
        choices = result.get("choices")
        if not isinstance(choices, list) or not choices:
            return None

        message = choices[0].get("message")
        if not isinstance(message, dict):
            return None

        return message.get("content")

    def _parse_ai_response(self, content: Any) -> Dict[str, Any]:
        if isinstance(content, list):
            text_parts: List[str] = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(str(part.get("text", "")))
            content = "\n".join(text_parts)

        if not isinstance(content, str):
            return {}

        text = content.strip()

        markdown_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if markdown_match:
            text = markdown_match.group(1).strip()

        candidates = [text]

        array_match = re.search(r"\[[\s\S]*\]", text)
        if array_match:
            candidates.append(array_match.group(0).strip())

        object_match = re.search(r"\{[\s\S]*\}", text)
        if object_match:
            candidates.append(object_match.group(0).strip())

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue

            normalized = self._normalize_guide(parsed)
            if normalized.get("steps"):
                return normalized

        return {}

    def _normalize_guide(self, data: Any) -> Dict[str, Any]:
        title = "操作引导"
        summary = "请按以下步骤操作。"
        estimated_time = "约3分钟"
        difficulty = "初级"
        prerequisites: List[str] = []
        common_mistakes: List[str] = []
        final_check: List[str] = []
        raw_steps: Any = data

        if isinstance(data, dict):
            raw_steps = data.get("steps", [])
            title_text = data.get("title")
            summary_text = data.get("summary")
            estimated_time_text = data.get("estimated_time")
            difficulty_text = data.get("difficulty")
            if isinstance(title_text, str) and title_text.strip():
                title = title_text.strip()
            if isinstance(summary_text, str) and summary_text.strip():
                summary = summary_text.strip()
            if isinstance(estimated_time_text, str) and estimated_time_text.strip():
                estimated_time = estimated_time_text.strip()
            if isinstance(difficulty_text, str) and difficulty_text.strip():
                difficulty = difficulty_text.strip()

            prerequisites = self._normalize_string_list(data.get("prerequisites"))
            common_mistakes = self._normalize_string_list(data.get("common_mistakes"))
            final_check = self._normalize_string_list(data.get("final_check"))

        steps = self._normalize_steps(raw_steps)
        if not prerequisites:
            prerequisites = ["确认网络连接稳定。", "准备好登录账号或必要权限。"]
        if not common_mistakes:
            common_mistakes = ["跳过关键确认步骤，导致结果与预期不一致。"]
        if not final_check:
            final_check = ["确认目标操作已经成功完成。", "如结果异常，返回上一步重新检查输入。"]

        return {
            "title": title,
            "summary": summary,
            "estimated_time": estimated_time,
            "difficulty": difficulty,
            "prerequisites": prerequisites,
            "steps": steps,
            "common_mistakes": common_mistakes,
            "final_check": final_check,
        }

    def _normalize_steps(self, raw_steps: Any) -> List[Dict[str, Any]]:
        if not isinstance(raw_steps, list):
            return []

        steps: List[Dict[str, Any]] = []
        for index, item in enumerate(raw_steps, start=1):
            if not isinstance(item, dict):
                continue

            rect = item.get("rect") or {}
            if not isinstance(rect, dict):
                rect = {}

            step_num = item.get("step")
            if not isinstance(step_num, int):
                step_num = index

            step_title = self._get_text_field(item, ["title", "name", "step_title"]) or f"步骤 {step_num}"
            description = self._build_chinese_description(item, step_num)
            purpose = self._get_text_field(item, ["purpose", "goal", "reason"])
            expected_result = self._get_text_field(item, ["expected_result", "result", "outcome"])
            tip = self._get_text_field(item, ["tip", "note"])
            warning = self._get_text_field(item, ["warning", "risk", "caution"])

            color = item.get("color")
            if not isinstance(color, str) or not color.strip():
                color = "#ff0000"

            normalized_rect = {
                "x": int(rect.get("x", 0) or 0),
                "y": int(rect.get("y", 0) or 0),
                "width": int(rect.get("width", 120) or 120),
                "height": int(rect.get("height", 40) or 40),
            }

            steps.append(
                {
                    "step": step_num,
                    "title": step_title,
                    "description": description,
                    "purpose": purpose,
                    "expected_result": expected_result,
                    "tip": tip,
                    "warning": warning,
                    "rect": normalized_rect,
                    "color": color.strip(),
                }
            )

        return steps

    def _normalize_string_list(self, value: Any) -> List[str]:
        if not isinstance(value, list):
            return []
        output: List[str] = []
        for item in value:
            if isinstance(item, str) and item.strip():
                output.append(item.strip())
        return output[:6]

    def _get_text_field(self, item: Dict[str, Any], keys: List[str]) -> Optional[str]:
        for key in keys:
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return None

    def _build_chinese_description(self, item: Dict[str, Any], step_num: int) -> str:
        primary = self._get_text_field(
            item,
            ["description", "action", "instruction", "content", "title"],
        )
        if not primary:
            primary = f"完成第 {step_num} 步操作。"

        extra_parts: List[str] = []
        for key in ["target", "result", "tip", "note"]:
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                extra_parts.append(value.strip())

        description = primary.strip().replace("\n", " ")
        if extra_parts:
            detail = "；".join(extra_parts[:2])
            if detail not in description:
                description = f"{description}（{detail}）"

        if not re.search(r"[\u4e00-\u9fff]", description):
            description = f"请执行该步骤：{description}"

        return description

    def _error_or_mock(self, error: str, raw_response: Optional[str] = None) -> Dict[str, Any]:
        if self.allow_mock_fallback:
            return {
                "success": True,
                "steps": self._get_mock_steps(),
                "title": "示例操作引导",
                "summary": "当前使用回退说明，请按步骤依次操作。",
                "estimated_time": "约3分钟",
                "difficulty": "初级",
                "prerequisites": ["确认网络状态正常。", "确保你在目标页面且有操作权限。"],
                "common_mistakes": ["遗漏关键按钮点击。", "输入信息后未确认提交。"],
                "final_check": ["目标页面已正确跳转。", "关键操作已生效。"],
                "ai_used": False,
                "source": "mock",
                "error": error,
                "raw_response": raw_response,
            }

        return {
            "success": False,
            "steps": [],
            "ai_used": False,
            "source": "error",
            "error": error,
            "raw_response": raw_response,
        }

    def _get_mock_steps(self) -> List[Dict[str, Any]]:
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
                "description": "在密码输入框中输入密码，并确认没有输错。",
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

    def test_connection(self) -> Dict[str, Any]:
        if not self.api_key:
            return {
                "success": False,
                "status": "missing_api_key",
                "message": "请在环境变量或 .env 中配置 DASHSCOPE_API_KEY",
            }

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with: connected",
                    }
                ],
                "max_tokens": 16,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=15,
            )

            if response.status_code == 200:
                return {
                    "success": True,
                    "status": "connected",
                    "model": self.model,
                    "message": "Qwen API 连接正常",
                }

            return {
                "success": False,
                "status": f"http_{response.status_code}",
                "message": response.text[:300],
            }
        except Exception as exc:
            return {
                "success": False,
                "status": "exception",
                "message": str(exc),
            }


def create_ai_service() -> QwenVLService:
    return QwenVLService()
