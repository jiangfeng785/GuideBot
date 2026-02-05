from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import base64
from werkzeug.utils import secure_filename
import uuid
import json

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许所有跨域请求（开发阶段）

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """检查文件格式是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_base64_image(base64_str, filename):
    """保存Base64图片到文件"""
    try:
        # 提取Base64数据部分
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        
        # 解码Base64
        image_data = base64.b64decode(base64_str)
        
        # 生成唯一文件名
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # 保存文件
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return filepath
    except Exception as e:
        print(f"保存图片失败: {e}")
        return None

# ===================== API路由 =====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'GuideBot Backend',
        'version': '1.0.0',
        'endpoints': [
            '/api/health',
            '/api/process/image',
            '/api/process/url',
            '/api/process/text',
            '/api/community/guides',
            '/api/community/share'
        ]
    })

@app.route('/api/process/image', methods=['POST'])
def process_image():
    """处理图片上传 - 核心API"""
    try:
        # 获取图片数据
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': '请提供图片数据'
            }), 400
        
        # 获取图片Base64数据
        image_base64 = data['image']
        
        # 生成文件名
        filename = f"{uuid.uuid4().hex}.png"
        filepath = save_base64_image(image_base64, filename)
        
        if not filepath:
            return jsonify({
                'success': False,
                'error': '保存图片失败'
            }), 500
        
        # ====== 这里应该调用AI API，但现在用模拟数据 ======
        # 实际项目这里会调用Qwen-VL API
        # ai_result = call_qwen_vl(filepath)
        # steps = parse_ai_result(ai_result)
        # ==============================================
        
        # 使用模拟数据
        steps = [
            {
                'step': 1,
                'description': '点击右上角的登录按钮',
                'rect': {'x': 650, 'y': 50, 'width': 100, 'height': 40},
                'color': '#ff0000'
            },
            {
                'step': 2,
                'description': '在用户名输入框输入账号',
                'rect': {'x': 300, 'y': 200, 'width': 200, 'height': 40},
                'color': '#00aa00'
            },
            {
                'step': 3,
                'description': '在密码输入框输入密码',
                'rect': {'x': 300, 'y': 260, 'width': 200, 'height': 40},
                'color': '#0000ff'
            },
            {
                'step': 4,
                'description': '点击登录确认按钮',
                'rect': {'x': 350, 'y': 350, 'width': 120, 'height': 45},
                'color': '#ff8800'
            }
        ]
        
        # 读取图片返回Base64（用于前端显示）
        with open(filepath, 'rb') as f:
            image_bytes = f.read()
        image_data_url = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        
        # 清理临时文件
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'steps': steps,
            'image': image_data_url,  # 返回图片用于前端显示
            'message': '图片处理完成，共生成4个步骤',
            'ai_used': False  # 标记是否使用了真实AI
        })
        
    except Exception as e:
        print(f"处理图片时出错: {e}")
        return jsonify({
            'success': False,
            'error': f'服务器内部错误: {str(e)}'
        }), 500

@app.route('/api/process/url', methods=['POST'])
def process_url():
    """处理网址输入"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': '请提供网址'
            }), 400
        
        # 这里应该实现网页截图功能
        # 实际项目可以使用 selenium 或 puppeteer
        # screenshot_path = capture_webpage(url)
        
        # 返回模拟数据
        steps = [
            {
                'step': 1,
                'description': f'打开网址: {url[:30]}...',
                'rect': {'x': 100, 'y': 100, 'width': 300, 'height': 50},
                'color': '#ff0000'
            },
            {
                'step': 2,
                'description': '等待页面完全加载',
                'rect': {'x': 150, 'y': 200, 'width': 250, 'height': 40},
                'color': '#00aa00'
            },
            {
                'step': 3,
                'description': '寻找目标功能或内容',
                'rect': {'x': 200, 'y': 300, 'width': 200, 'height': 60},
                'color': '#0000ff'
            }
        ]
        
        return jsonify({
            'success': True,
            'steps': steps,
            'url': url,
            'message': '网址处理完成（模拟数据）',
            'note': '实际功能需要集成网页截图功能'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'处理网址失败: {str(e)}'
        }), 500

@app.route('/api/process/text', methods=['POST'])
def process_text():
    """处理文本描述"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': '请提供文本描述'
            }), 400
        
        # 根据文本生成不同的步骤
        if '微信' in text and '朋友圈' in text:
            steps = [
                {
                    'step': 1,
                    'description': '打开手机微信应用',
                    'rect': {'x': 100, 'y': 100, 'width': 60, 'height': 60},
                    'color': '#07c160'
                },
                {
                    'step': 2,
                    'description': '点击底部"发现"标签',
                    'rect': {'x': 200, 'y': 600, 'width': 60, 'height': 30},
                    'color': '#07c160'
                },
                {
                    'step': 3,
                    'description': '点击"朋友圈"入口',
                    'rect': {'x': 150, 'y': 300, 'width': 100, 'height': 30},
                    'color': '#07c160'
                }
            ]
            scenario = '微信发朋友圈'
        elif '抢课' in text or '选课' in text:
            steps = [
                {
                    'step': 1,
                    'description': '登录学校教务系统',
                    'rect': {'x': 100, 'y': 100, 'width': 80, 'height': 30},
                    'color': '#0066cc'
                },
                {
                    'step': 2,
                    'description': '进入选课页面',
                    'rect': {'x': 200, 'y': 200, 'width': 100, 'height': 30},
                    'color': '#0066cc'
                },
                {
                    'step': 3,
                    'description': '选择目标课程并确认',
                    'rect': {'x': 150, 'y': 300, 'width': 120, 'height': 30},
                    'color': '#0066cc'
                }
            ]
            scenario = '学校选课系统'
        else:
            steps = [
                {
                    'step': 1,
                    'description': '打开相关应用/网站',
                    'rect': {'x': 100, 'y': 100, 'width': 100, 'height': 50},
                    'color': '#ff6600'
                },
                {
                    'step': 2,
                    'description': '找到功能入口或相关按钮',
                    'rect': {'x': 200, 'y': 200, 'width': 100, 'height': 30},
                    'color': '#ff6600'
                },
                {
                    'step': 3,
                    'description': '按照提示完成操作',
                    'rect': {'x': 150, 'y': 300, 'width': 150, 'height': 40},
                    'color': '#ff6600'
                }
            ]
            scenario = '通用操作'
        
        return jsonify({
            'success': True,
            'steps': steps,
            'text': text,
            'scenario': scenario,
            'message': f'已为您生成"{scenario}"操作指引'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'处理文本失败: {str(e)}'
        }), 500

@app.route('/api/community/guides', methods=['GET'])
def get_community_guides():
    """获取社区分享的指引"""
    # 模拟社区数据
    guides = [
        {
            'id': 1,
            'title': '微信发朋友圈详细步骤',
            'author': '张三',
            'likes': 42,
            'steps': 3,
            'created_at': '2024-01-15',
            'scenario': '微信功能'
        },
        {
            'id': 2,
            'title': '学校教务系统抢课指南',
            'author': '李四',
            'likes': 28,
            'steps': 4,
            'created_at': '2024-01-20',
            'scenario': '教育系统'
        },
        {
            'id': 3,
            'title': '淘宝APP查找商品技巧',
            'author': '王五',
            'likes': 15,
            'steps': 5,
            'created_at': '2024-01-25',
            'scenario': '电商购物'
        }
    ]
    
    return jsonify({
        'success': True,
        'guides': guides,
        'total': len(guides),
        'message': '社区热门指引'
    })

@app.route('/api/community/share', methods=['POST'])
def share_to_community():
    """分享指引到社区"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data or 'steps' not in data:
            return jsonify({
                'success': False,
                'error': '请提供标题和步骤数据'
            }), 400
        
        # 在实际项目中，这里会将数据保存到数据库
        # 这里只是模拟保存成功
        
        return jsonify({
            'success': True,
            'message': '分享成功！您的指引已发布到社区',
            'share_id': str(uuid.uuid4().hex),
            'timestamp': '2024-01-30T10:30:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'分享失败: {str(e)}'
        }), 500

@app.route('/api/test/ai', methods=['GET'])
def test_ai_connection():
    """测试AI API连接（模拟）"""
    return jsonify({
        'success': True,
        'ai_service': 'Qwen-VL (模拟)',
        'status': '可用',
        'note': '实际项目需配置真实的Qwen-VL API Key',
        'config_steps': [
            '1. 注册阿里云百炼平台',
            '2. 获取API Key',
            '3. 在backend/utils/ai_service.py中配置',
            '4. 调用真实的AI API'
        ]
    })

# ===================== 辅助路由 =====================

@app.route('/api/info', methods=['GET'])
def api_info():
    """获取API信息"""
    return jsonify({
        'name': 'GuideBot API',
        'description': '智能操作指引生成器后端API',
        'version': '1.0.0',
        'author': '计算机系科创项目组',
        'endpoints': {
            'GET': [
                '/api/health - 健康检查',
                '/api/community/guides - 获取社区指引',
                '/api/test/ai - 测试AI连接',
                '/api/info - 本信息页'
            ],
            'POST': [
                '/api/process/image - 处理图片',
                '/api/process/url - 处理网址',
                '/api/process/text - 处理文本',
                '/api/community/share - 分享到社区'
            ]
        }
    })

# ===================== 启动应用 =====================

if __name__ == '__main__':
    print("=" * 50)
    print("GuideBot 后端服务启动")
    print("访问 http://localhost:5000/api/health 测试连接")
    print("API文档: http://localhost:5000/api/info")
    print("=" * 50)
    
    app.run(
        debug=True, 
        port=5000, 
        host='0.0.0.0',
        use_reloader=True
    )