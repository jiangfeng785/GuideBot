from __future__ import annotations

import base64
import json
import os
import re
<<<<<<< HEAD
<<<<<<< HEAD
=======
import time
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
from typing import Any, Dict, List, Optional

import requests


def _load_env_if_available() -> None:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    """Load .env from python-dotenv if available, else parse manually."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(env_path)
        return
    except Exception:
        pass

    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("'").strip('"')
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        return
<<<<<<< HEAD
=======
    """Load .env if python-dotenv exists; skip silently otherwise."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return

    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76


class QwenVLService:
    def __init__(self, api_key: Optional[str] = None):
        _load_env_if_available()

        self.api_key = (api_key or os.getenv("DASHSCOPE_API_KEY") or "").strip()
        self.base_url = (
            os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1").rstrip("/")
        )
        self.model = os.getenv("DASHSCOPE_MODEL", "qwen-max")
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        self.vision_model = os.getenv("DASHSCOPE_VISION_MODEL", "qwen-vl-max-latest").strip() or self.model
        self.allow_mock_fallback = self._parse_bool(os.getenv("AI_ALLOW_MOCK_FALLBACK"), True)
        self.reasoning_effort = (os.getenv("AI_REASONING_EFFORT", "high") or "high").strip().lower()
        self.guide_style = (os.getenv("AI_GUIDE_STYLE", "friendly_detailed") or "friendly_detailed").strip().lower()
        self.temperature = self._parse_float(os.getenv("AI_TEMPERATURE"), 0.35)
        self.max_tokens = self._parse_int(os.getenv("AI_MAX_TOKENS"), 1800)
        self.thinking_budget = self._parse_int(os.getenv("AI_THINKING_BUDGET"), 2048)
        self.request_timeout = self._parse_int(os.getenv("AI_REQUEST_TIMEOUT"), 75)
<<<<<<< HEAD
=======
        self.allow_mock_fallback = self._parse_bool(os.getenv("AI_ALLOW_MOCK_FALLBACK"), True)
        self.request_timeout_seconds = self._parse_int(os.getenv("AI_REQUEST_TIMEOUT_SECONDS"), 90)
        self.request_retries = self._parse_int(os.getenv("AI_REQUEST_RETRIES"), 1)
        self.retry_backoff_seconds = self._parse_float(os.getenv("AI_REQUEST_RETRY_BACKOFF_SECONDS"), 1.5)
        self.image_max_tokens = self._parse_int(os.getenv("AI_IMAGE_MAX_TOKENS"), 1800)
        self.text_max_tokens = self._parse_int(os.getenv("AI_TEXT_MAX_TOKENS"), 1300)
        self.url_max_tokens = self._parse_int(os.getenv("AI_URL_MAX_TOKENS"), 1300)
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

    @staticmethod
    def _parse_bool(value: Optional[str], default: bool = True) -> bool:
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    def _parse_float(value: Optional[str], default: float) -> float:
        if value is None:
            return default
        try:
            return float(value.strip())
        except Exception:
            return default

    @staticmethod
<<<<<<< HEAD
=======
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    def _parse_int(value: Optional[str], default: int) -> int:
        if value is None:
            return default
        try:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
            return int(value.strip())
        except Exception:
            return default

    def _build_prompt(self, scene_info: Optional[Dict[str, Any]] = None, user_note: str = "") -> str:
        style_hint = "语气亲和、像耐心老师带着新手一步一步完成"
        if self.guide_style == "concise":
            style_hint = "语气专业简洁，避免冗余"
        elif self.guide_style == "expert":
            style_hint = "语气专业且深入，强调判断标准和风险提示"
        scene_text = ""
        if scene_info:
            scene_text = f"场景分析结果（你必须基于它生成步骤）：{json.dumps(scene_info, ensure_ascii=False)}。"
        note_text = ""
        cleaned_note = user_note.strip()
        if cleaned_note:
            note_text = (
                f"用户补充问题：{cleaned_note}。"
                "请将该问题作为任务目标，但不能替代读图。"
                "你必须先基于截图识别页面元素，再给出步骤。"
            )

        return (
            "你是一位资深中文产品导师与操作教练。"
            "请先在内部完成观察与推理，再输出最终答案。"
            "输出必须是严格 JSON，禁止输出任何 JSON 之外的内容。"
            "请根据图片内容生成用户可直接照做的引导文案。"
            "你输出的是给终端用户执行的步骤，不是解释你如何分析图片，也不是讲解如何编写 JSON。"
            f"{scene_text}"
            f"{note_text}"
            f"写作风格：{style_hint}。"
            "字段格式必须为："
            "{"
            "\"title\":\"简洁标题\","
            "\"summary\":\"2-3句说明，先共情当前任务，再说明整体路径\","
            "\"estimated_time\":\"如 约5分钟\","
            "\"difficulty\":\"初级/中级/高级\","
            "\"prerequisites\":[\"前置条件1\",\"前置条件2\"],"
            "\"steps\":["
            "{"
            "\"step\":1,"
            "\"title\":\"步骤小标题\","
            "\"description\":\"详细动作说明，必须是简体中文完整句子，建议2-3句\","
            "\"purpose\":\"这一步为什么做\","
            "\"expected_result\":\"完成后你会看到什么\","
            "\"tip\":\"可选，实用小技巧\","
            "\"warning\":\"可选，避坑提醒\","
            "\"rect\":{\"x\":0,\"y\":0,\"width\":120,\"height\":40},"
            "\"color\":\"#ff0000\""
            "}"
            "],"
            "\"common_mistakes\":[\"常见错误1\"],"
            "\"final_check\":[\"完成检查点1\"]"
            "}"
            "要求："
            "1) 所有可读文本必须是简体中文。"
            "2) 步骤建议 4-8 步，每步聚焦单一动作。"
            "3) 每步优先包含“操作动作 + 判断是否成功 + 下一步衔接”。"
            "4) 避免空话与口号，必须给可执行细节。"
            "5) 严禁输出“先观察图片/生成指南/按字段填写JSON/示例内容”等元步骤。"
            "6) 若有用户备注，必须把步骤锚定到截图可见元素（如按钮、输入框、菜单、图标、区域位置）。"
            "7) 若备注与截图不一致，以截图可见信息为准，并在 warning 说明冲突点。"
            "8) 若截图不是可操作界面（例如风景照/实物图），不要编造网站或App按钮，应改为图像解读与可执行建议。"
        )

    def _build_text_prompt(self, source_type: str, source_text: str, scene_info: Optional[Dict[str, Any]] = None) -> str:
        source_label = "网址" if source_type == "url" else "文本描述"
        scene_text = ""
        if scene_info:
            scene_text = f"任务分析结果（你必须基于它生成步骤）：{json.dumps(scene_info, ensure_ascii=False)}。"
        if source_type == "url":
            scenario_intro = (
                "你的任务是写“手把手网站使用教程”。"
                "默认用户是第一次使用该网站、对页面结构不熟。"
            )
            scenario_requirements = (
                "网址场景强制要求："
                "1) 第1步必须是“打开网址并确认进入正确页面”。"
                "2) 后续按“找入口 -> 点击进入 -> 填写/选择 -> 提交 -> 结果确认”组织。"
                "3) 每步 description 使用新手口吻，清楚写出先做什么、看到什么、下一步做什么。"
                "4) 至少包含 1 条异常处理（如找不到按钮/页面加载失败/账号校验失败）。"
                "5) 步骤建议 5-9 步。"
            )
        else:
            scenario_intro = "请根据用户文本描述生成可执行引导。"
            scenario_requirements = "步骤建议 4-8 步，每步聚焦一个动作。"
        return (
            "你是一位资深中文产品导师与操作教练。"
            "请先在内部完成推理，再输出最终答案。"
            "输出必须是严格 JSON，禁止输出任何 JSON 以外的内容。"
            f"用户提供的是{source_label}，请据此生成可执行引导。"
            f"{scenario_intro}"
            "不要假装你看到了页面截图；若信息不足，请给稳妥且可执行的通用流程，并标出关键判断点。"
            f"用户输入：{source_text}"
            f"{scene_text}"
            "字段格式必须为："
            "{"
            "\"title\":\"简洁标题\","
            "\"summary\":\"2-3句说明，先共情当前任务，再说明整体路径\","
            "\"estimated_time\":\"如 约5分钟\","
            "\"difficulty\":\"初级/中级/高级\","
            "\"prerequisites\":[\"前置条件1\",\"前置条件2\"],"
            "\"steps\":["
            "{"
            "\"step\":1,"
            "\"title\":\"步骤小标题\","
            "\"description\":\"详细动作说明，必须是简体中文完整句子，建议2-3句\","
            "\"purpose\":\"这一步为什么做\","
            "\"expected_result\":\"完成后你会看到什么\","
            "\"tip\":\"可选，实用小技巧\","
            "\"warning\":\"可选，避坑提醒\","
            "\"rect\":{\"x\":0,\"y\":0,\"width\":120,\"height\":40},"
            "\"color\":\"#ff0000\""
            "}"
            "],"
            "\"common_mistakes\":[\"常见错误1\"],"
            "\"final_check\":[\"完成检查点1\"]"
            "}"
            "要求："
            "1) 所有可读文本必须是简体中文。"
            f"2) {scenario_requirements}"
            "3) 每步优先包含“操作动作 + 判断是否成功 + 下一步衔接”。"
            "4) 避免空话与口号，必须给可执行细节。"
            "5) 严禁输出“生成指南/按字段填写JSON/示例内容”等元步骤。"
        )

    def _build_retry_prompt(self, scene_info: Optional[Dict[str, Any]] = None, user_note: str = "") -> str:
        strict_note_hint = ""
        if user_note.strip():
            strict_note_hint = (
                "上一次结果疑似未读图。"
                "本次必须显式引用截图中的可见元素或区域位置，禁止只围绕备注泛化输出。"
            )
        return (
            self._build_prompt(scene_info, user_note=user_note)
            + "上一次输出偏向模板或示例。"
            + "请严格改为“真实用户可直接执行”的任务步骤。"
            + "如果图片不是可操作界面，请输出“图像解读引导”，同样要具体可执行。"
            + strict_note_hint
        )

    def _build_text_retry_prompt(self, source_type: str, source_text: str, scene_info: Optional[Dict[str, Any]] = None) -> str:
        retry_hint = "请严格改为“真实用户可直接执行”的任务步骤。"
        if source_type == "url":
            retry_hint = (
                "请改写为“手把手网站使用教程”，像老师带新手实操。"
                "不要讲抽象方法论，不要写‘观察图片/规划步骤’这类元叙述。"
            )
        return (
            self._build_text_prompt(source_type, source_text, scene_info)
            + "上一次输出偏向模板或示例。"
            + retry_hint
        )

    def _build_scene_prompt(self) -> str:
        return (
            "你是图像任务分析器。请先观察图片，再只输出 JSON："
            "{"
            "\"scene_type\":\"ui/document/natural/other\","
            "\"intent\":\"一句话说明用户最可能想完成的任务\","
            "\"key_objects\":[\"关键对象1\",\"关键对象2\"],"
            "\"recommended_mode\":\"operation_guide 或 interpretation_guide\""
            "}"
            "要求："
            "1) 只输出 JSON。"
            "2) 不要输出模板示例解释。"
            "3) 文本使用简体中文。"
        )

    def _build_text_scene_prompt(self, source_type: str, source_text: str) -> str:
        source_label = "网址" if source_type == "url" else "文本描述"
        extra_hint = ""
        if source_type == "url":
            extra_hint = "并优先识别“首次使用该网站时，用户最可能要完成的核心任务”。"
        return (
            f"你是任务分析器。用户输入的是{source_label}，请只输出 JSON："
            "{"
            "\"intent\":\"一句话说明用户最可能想完成的任务\","
            "\"task_type\":\"web_task/app_task/account_task/content_task/other\","
            "\"risk_points\":[\"风险点1\",\"风险点2\"],"
            "\"recommended_mode\":\"operation_guide\""
            "}"
            f"用户输入：{source_text}"
            f"{extra_hint}"
            "要求："
            "1) 只输出 JSON。"
            "2) 文本使用简体中文。"
        )

    def _call_completion(
        self,
        prompt: str,
        image_base64: Optional[str] = None,
        image_mime: str = "image/png",
        model_override: Optional[str] = None,
    ) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        content_parts: List[Dict[str, Any]] = []
        if image_base64:
            content_parts.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:{image_mime};base64,{image_base64}"},
                }
            )
        content_parts.append({"type": "text", "text": prompt})

        payload = {
            "model": model_override or self.model,
            "messages": [
                {
                    "role": "user",
                    "content": content_parts,
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if self.reasoning_effort in {"low", "medium", "high"}:
            payload["reasoning_effort"] = self.reasoning_effort
        if self.thinking_budget > 0:
            payload["thinking_budget"] = self.thinking_budget

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.request_timeout,
        )
        if response.status_code >= 400 and "reasoning_effort" in payload:
            fallback_payload = dict(payload)
            fallback_payload.pop("reasoning_effort", None)
            fallback_payload.pop("thinking_budget", None)
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=fallback_payload,
                timeout=self.request_timeout,
            )
        if response.status_code >= 400 and model_override:
            fallback_model_payload = dict(payload)
            fallback_model_payload["model"] = self.model
            fallback_model_payload.pop("reasoning_effort", None)
            fallback_model_payload.pop("thinking_budget", None)
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=fallback_model_payload,
                timeout=self.request_timeout,
            )
        return response

    def _analyze_scene(self, image_base64: str, image_mime: str) -> Dict[str, Any]:
        response = self._call_completion(
            self._build_scene_prompt(),
            image_base64=image_base64,
            image_mime=image_mime,
            model_override=self.vision_model,
        )
        if response.status_code != 200:
            return {}
        result = response.json()
        content = self._extract_content(result)
        parsed = self._parse_json_loose(content)
        if not isinstance(parsed, dict):
            return {}
        scene_type = str(parsed.get("scene_type") or "").strip().lower()
        if scene_type not in {"ui", "document", "natural", "other"}:
            scene_type = "other"
        intent = str(parsed.get("intent") or "").strip()
        recommended_mode = str(parsed.get("recommended_mode") or "").strip().lower()
        if recommended_mode not in {"operation_guide", "interpretation_guide"}:
            recommended_mode = "operation_guide"
        key_objects = parsed.get("key_objects")
        if not isinstance(key_objects, list):
            key_objects = []
        key_objects = [str(x).strip() for x in key_objects if str(x).strip()][:6]
        return {
            "scene_type": scene_type,
            "intent": intent,
            "recommended_mode": recommended_mode,
            "key_objects": key_objects,
        }

    def _analyze_text_scene(self, source_type: str, source_text: str) -> Dict[str, Any]:
        response = self._call_completion(self._build_text_scene_prompt(source_type, source_text))
        if response.status_code != 200:
            return {}
        result = response.json()
        content = self._extract_content(result)
        parsed = self._parse_json_loose(content)
        if not isinstance(parsed, dict):
            return {}
        intent = str(parsed.get("intent") or "").strip()
        task_type = str(parsed.get("task_type") or "").strip().lower()
        if task_type not in {"web_task", "app_task", "account_task", "content_task", "other"}:
            task_type = "other"
        risk_points = parsed.get("risk_points")
        if not isinstance(risk_points, list):
            risk_points = []
        risk_points = [str(x).strip() for x in risk_points if str(x).strip()][:6]
        recommended_mode = str(parsed.get("recommended_mode") or "").strip().lower() or "operation_guide"
        return {
            "intent": intent,
            "task_type": task_type,
            "risk_points": risk_points,
            "recommended_mode": recommended_mode,
        }

    def _is_template_like_guide(self, guide: Dict[str, Any]) -> bool:
        steps = guide.get("steps", [])
        if not isinstance(steps, list) or not steps:
            return True

        text_chunks: List[str] = []
        summary = guide.get("summary")
        if isinstance(summary, str):
            text_chunks.append(summary)
        title = guide.get("title")
        if isinstance(title, str):
            text_chunks.append(title)
        for step in steps[:5]:
            if isinstance(step, dict):
                for key in ("title", "description", "purpose"):
                    value = step.get(key)
                    if isinstance(value, str):
                        text_chunks.append(value)

        merged = " ".join(text_chunks)
        patterns = [
            r"观察.*图片",
            r"图片分析",
            r"指南生成",
            r"编写\s*json",
            r"字段格式",
            r"示例(数据|内容)",
            r"根据.*图片.*生成",
            r"创建.*操作手册",
        ]
        hit_count = sum(1 for p in patterns if re.search(p, merged, flags=re.IGNORECASE))
        return hit_count >= 2

    def _is_image_grounded_guide(self, guide: Dict[str, Any], scene_info: Optional[Dict[str, Any]]) -> bool:
        steps = guide.get("steps", [])
        if not isinstance(steps, list) or not steps:
            return False

        chunks: List[str] = []
        for key in ("title", "summary"):
            value = guide.get(key)
            if isinstance(value, str) and value.strip():
                chunks.append(value.strip())
        for step in steps[:6]:
            if isinstance(step, dict):
                for key in ("title", "description", "expected_result", "warning"):
                    value = step.get(key)
                    if isinstance(value, str) and value.strip():
                        chunks.append(value.strip())
        merged = " ".join(chunks)

        anchor_patterns = [
            r"按钮",
            r"输入框",
            r"搜索框",
            r"菜单",
            r"图标",
            r"右上角|左上角|底部|顶部|中间",
            r"页面",
            r"导航",
            r"栏",
            r"点击|输入|选择|提交",
        ]
        anchor_hit = sum(1 for p in anchor_patterns if re.search(p, merged))

        scene_keys: List[str] = []
        if isinstance(scene_info, dict):
            raw_keys = scene_info.get("key_objects")
            if isinstance(raw_keys, list):
                scene_keys = [str(v).strip() for v in raw_keys if isinstance(v, str) and v.strip()]
        key_hit = sum(1 for key in scene_keys if key and key in merged)

        if scene_keys:
            return key_hit >= 1 or anchor_hit >= 2
        return anchor_hit >= 2
<<<<<<< HEAD
=======
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
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

    def encode_image_to_base64(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    def _detect_image_mime(self, image_path: str) -> str:
        try:
            with open(image_path, "rb") as f:
                head = f.read(16)
        except Exception:
            return "image/png"

        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if head.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if head.startswith(b"GIF87a") or head.startswith(b"GIF89a"):
            return "image/gif"
        if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
            return "image/webp"
        if head.startswith(b"BM"):
            return "image/bmp"
        return "image/png"

    def analyze_image(self, image_path: str, user_note: str = "") -> Dict[str, Any]:
<<<<<<< HEAD
=======
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
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        if not os.path.exists(image_path):
            return self._error_or_mock(f"图片文件不存在: {image_path}")

        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")

        try:
            image_base64 = self.encode_image_to_base64(image_path)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
            image_mime = self._detect_image_mime(image_path)
            scene_info = self._analyze_scene(image_base64, image_mime=image_mime)
            response = self._call_completion(
                self._build_prompt(scene_info, user_note=user_note),
                image_base64=image_base64,
                image_mime=image_mime,
                model_override=self.vision_model,
            )

            if response.status_code != 200:
                return self._error_or_mock(
                    f"AI API error {response.status_code}: {response.text[:300]}"
                )

            result = response.json()
            content = self._extract_content(result)
            if content is None:
                return self._error_or_mock(
                    "AI 响应缺少必要字段（choices/message/content）",
                    raw_response=json.dumps(result, ensure_ascii=False)[:1000],
                )

            guide = self._parse_ai_response(content)
            steps = guide.get("steps", [])
            require_grounding = bool(user_note.strip())
            if self._is_template_like_guide(guide) or (
                require_grounding and not self._is_image_grounded_guide(guide, scene_info)
            ):
                retry_response = self._call_completion(
                    self._build_retry_prompt(scene_info, user_note=user_note),
                    image_base64=image_base64,
                    image_mime=image_mime,
                    model_override=self.vision_model,
                )
                if retry_response.status_code == 200:
                    retry_result = retry_response.json()
                    retry_content = self._extract_content(retry_result)
                    if retry_content is not None:
                        retried_guide = self._parse_ai_response(retry_content)
                        retried_ok = retried_guide.get("steps") and not self._is_template_like_guide(retried_guide)
                        if retried_ok and (
                            (not require_grounding)
                            or self._is_image_grounded_guide(retried_guide, scene_info)
                        ):
                            guide = retried_guide
                            steps = guide.get("steps", [])
            if self._is_template_like_guide(guide):
                return self._error_or_mock(
                    "AI 返回了模板化示例内容，请上传更清晰的任务截图（包含按钮/输入框/菜单）后重试。",
                    raw_response=str(content)[:1000],
                    force_no_mock=True,
                )
            if require_grounding and not self._is_image_grounded_guide(guide, scene_info):
                return self._error_or_mock(
                    "AI 未能基于截图元素生成步骤，请换更清晰截图或缩小备注问题范围后重试。",
                    raw_response=str(content)[:1000],
                    force_no_mock=True,
                )

            if not steps:
                return self._error_or_mock(
                    "无法从 AI 响应中解析出有效步骤",
                    raw_response=str(content)[:1000],
                )

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
<<<<<<< HEAD
=======
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
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

        except requests.RequestException as exc:
            return self._error_or_mock(f"AI 请求失败: {exc}")
        except Exception as exc:
            return self._error_or_mock(f"AI 分析异常: {exc}")

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    def analyze_url(self, url: str) -> Dict[str, Any]:
        if not url.strip():
            return self._error_or_mock("缺少网址参数。", force_no_mock=True)
        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")
        return self._analyze_textual_input("url", url.strip())

    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return self._error_or_mock("缺少文本描述。", force_no_mock=True)
        if not self.api_key:
            return self._error_or_mock("未配置 DASHSCOPE_API_KEY")
        return self._analyze_textual_input("text", text.strip())

    def _analyze_textual_input(self, source_type: str, source_text: str) -> Dict[str, Any]:
        try:
            scene_info = self._analyze_text_scene(source_type, source_text)
            response = self._call_completion(self._build_text_prompt(source_type, source_text, scene_info))
            if response.status_code != 200:
                return self._error_or_mock(
                    f"AI API error {response.status_code}: {response.text[:300]}"
                )

            result = response.json()
            content = self._extract_content(result)
            if content is None:
                return self._error_or_mock(
                    "AI 响应缺少必要字段（choices/message/content）",
                    raw_response=json.dumps(result, ensure_ascii=False)[:1000],
                )

            guide = self._parse_ai_response(content)
            steps = guide.get("steps", [])
            if self._is_template_like_guide(guide):
                retry_response = self._call_completion(
                    self._build_text_retry_prompt(source_type, source_text, scene_info)
                )
                if retry_response.status_code == 200:
                    retry_result = retry_response.json()
                    retry_content = self._extract_content(retry_result)
                    if retry_content is not None:
                        retried_guide = self._parse_ai_response(retry_content)
                        if retried_guide.get("steps") and not self._is_template_like_guide(retried_guide):
                            guide = retried_guide
                            steps = guide.get("steps", [])
            if self._is_template_like_guide(guide):
                return self._error_or_mock(
                    "AI 返回了模板化示例内容，请补充更具体的任务目标后重试。",
                    raw_response=str(content)[:1000],
                    force_no_mock=True,
                )

            if not steps:
                return self._error_or_mock(
                    "无法从 AI 响应中解析出有效步骤",
                    raw_response=str(content)[:1000],
                )

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
<<<<<<< HEAD
=======
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
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
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
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        parsed = self._parse_json_loose(content)
        if parsed is None:
            return {}
        normalized = self._normalize_guide(parsed)
        if normalized.get("steps"):
            return normalized
        return {}

    def _parse_json_loose(self, content: Any) -> Optional[Any]:
<<<<<<< HEAD
=======
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        if isinstance(content, list):
            text_parts: List[str] = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(str(part.get("text", "")))
            content = "\n".join(text_parts)

        if not isinstance(content, str):
<<<<<<< HEAD
<<<<<<< HEAD
            return None
=======
            return {}
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
            return None
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

        text = content.strip()

        markdown_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if markdown_match:
            text = markdown_match.group(1).strip()

        candidates = [text]

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        for array_match in re.finditer(r"\[[\s\S]*?\]", text):
            candidates.append(array_match.group(0).strip())
            if len(candidates) >= 5:
                break

        for object_match in re.finditer(r"\{[\s\S]*?\}", text):
            candidates.append(object_match.group(0).strip())
            if len(candidates) >= 8:
                break
<<<<<<< HEAD
=======
        array_match = re.search(r"\[[\s\S]*\]", text)
        if array_match:
            candidates.append(array_match.group(0).strip())

        object_match = re.search(r"\{[\s\S]*\}", text)
        if object_match:
            candidates.append(object_match.group(0).strip())
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
                return parsed
            except json.JSONDecodeError:
                continue

        return None
<<<<<<< HEAD
=======
            except json.JSONDecodeError:
                continue

            normalized = self._normalize_guide(parsed)
            if normalized.get("steps"):
                return normalized

        return {}
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76

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

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
        if len(description) < 28:
            description = f"{description} 完成后先确认页面反馈正常，再继续下一步。"

        return description

    def _error_or_mock(
        self,
        error: str,
        raw_response: Optional[str] = None,
        force_no_mock: bool = False,
    ) -> Dict[str, Any]:
        if self.allow_mock_fallback and not force_no_mock:
<<<<<<< HEAD
=======
        return description

    def _error_or_mock(self, error: str, raw_response: Optional[str] = None) -> Dict[str, Any]:
        if self.allow_mock_fallback:
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
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
