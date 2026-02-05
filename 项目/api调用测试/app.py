from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 最简单的健康检查API
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': '后端API服务正常运行',
        'version': '1.0.0'
    })

# 模拟图片处理API（返回固定数据）
@app.route('/api/process/image', methods=['POST'])
def process_image():
    # 模拟AI处理结果
    result = {
        'success': True,
        'steps': [
            {
                'step': 1,
                'description': '点击登录按钮',
                'rect': {'x': 100, 'y': 100, 'width': 80, 'height': 30}
            },
            {
                'step': 2,
                'description': '输入用户名和密码',
                'rect': {'x': 150, 'y': 200, 'width': 200, 'height': 30}
            },
            {
                'step': 3,
                'description': '点击确认按钮',
                'rect': {'x': 200, 'y': 300, 'width': 100, 'height': 30}
            }
        ],
        'message': '这是模拟数据，实际会调用AI API'
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)