from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import re
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# ⚠ 建议把 key 放环境变量里，这个写死在代码里的 key 建议立刻去控制台里重置掉
QIANWEN_API_KEY = "sk-f8aefb83bcdf460d81cb433fcbcf2f4e"

# 初始化 OpenAI 客户端，指向千问的 compatible-mode
client = OpenAI(
    api_key=QIANWEN_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': '后端API服务正常运行',
        'version': '1.0.0'
    })


def is_valid_url(url):
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and pattern.match(url)


@app.route('/api/process/image', methods=['POST'])
def process_image():
    try:
        # 1. 获取前端 JSON 参数
        data = request.get_json()
        if not data or 'image_url' not in data:
            return jsonify({
                'success': False,
                'message': '缺少必要参数：image_url',
                'steps': []
            }), 400

        image_url = data.get('image_url')
        if not is_valid_url(image_url):
            return jsonify({
                'success': False,
                'message': 'image_url 格式不正确',
                'steps': []
            }), 400

        prompt = data.get(
            'prompt',
            '请分析这张图片，返回一个 JSON 对象，其中包含一个 steps 数组，每个元素包含 step、description、rect 字段。'
        )

        # 2. 调用千问（OpenAI 兼容接口）
        completion = client.chat.completions.create(
            model="qwen3-vl-plus",  # 或 qwen-vl-plus / qwen-vl-max 等
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            top_p=0.9
        )

        # 3. 解析返回（OpenAI 风格）
        content = completion.choices[0].message.content

        # 有的 SDK 版本多模态时 content 可能是 list，这里做个兼容
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
            content = "".join(text_parts)

        # 期望模型返回类似：
        # { "steps": [ { "step": 1, "description": "...", "rect": [x,y,w,h] }, ... ] }
        obj = json.loads(content)

        if isinstance(obj, dict):
            steps = obj.get("steps", [])
        else:
            # 万一你让模型直接返回数组，也兼容一下
            steps = obj

        return jsonify({
            'success': True,
            'message': '调用千问AI成功',
            'steps': steps
        })

    except json.JSONDecodeError as e:
        return jsonify({
            'success': False,
            'message': f'AI返回内容无法解析为JSON: {str(e)}\n原始内容: {str(content)[:200]}...',
            'steps': []
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'服务器内部错误: {str(e)}',
            'steps': []
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
