# GuideBot - 智能操作指引生成器

GuideBot 是一个基于 AI 的智能操作指引生成系统，能够通过分析用户提供的截图、网址或文本描述，自动生成详细的可视化操作步骤指南。

## 项目简介

GuideBot 利用先进的视觉语言模型（VLM），能够理解界面截图、识别操作元素，并生成用户友好的中文操作指引。无论是软件教程、网站使用指南，还是日常操作步骤，GuideBot 都能快速生成专业、易懂的指导文档。

## 核心功能

### 1. 多模态输入支持

- **截图上传分析**：上传界面截图，AI 自动识别页面元素并生成操作步骤
- **网址输入**：输入网址，生成网站使用教程
- **文本描述**：描述目标任务，生成操作指引

### 2. 智能分析能力

- **场景识别**：自动识别 UI 界面、文档、自然场景等不同类型
- **元素定位**：精准识别按钮、输入框、菜单等界面元素
- **任务理解**：理解用户意图，生成针对性的操作步骤

### 3. 可视化步骤展示

生成的指引包含丰富的信息：
- 步骤标题和详细描述
- 操作目的说明
- 预期结果展示
- 实用小技巧
- 避坑提醒
- 常见错误说明
- 完成检查点

### 4. 智能质量控制

- **模板检测**：自动识别并过滤模板化输出
- **图像锚定验证**：确保步骤基于截图中的可见元素
- **自动重试机制**：检测到问题时自动重新生成

## 技术架构

### 前端技术栈

- **纯原生实现**：HTML5 + CSS3 + JavaScript (ES6+)
- **响应式设计**：支持桌面端和移动端
- **拖拽上传**：支持图片拖拽上传
- **实时预览**：上传图片后立即预览

### 后端技术栈

- **Web 框架**：Flask 2.3+
- **跨域支持**：Flask-CORS
- **HTTP 客户端**：Requests

### AI 模型

- **视觉语言模型**：qwen-vl-max（阿里云通义千问视觉大模型）
- **API 服务**：阿里云 DashScope 兼容模式 API
- **推理能力**：支持图像理解、文本生成、场景分析

## 项目结构

```
GuideBot-main/
├── 项目/
│   ├── backend/                 # 后端服务
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── ai_service.py    # AI 服务核心实现
│   │   ├── .env                 # 环境配置文件
│   │   ├── app.py               # Flask 应用主文件
│   │   ├── requirements.txt     # Python 依赖
│   │   └── uploads/             # 临时文件上传目录
│   ├── frontend/                # 前端界面
│   │   ├── index.html           # 主页面
│   │   ├── style.css            # 样式文件
│   │   ├── app.js               # 应用逻辑
│   │   ├── api.js               # API 调用封装
│   │   ├── canvas.js            # Canvas 绘图工具
│   │   └── ui.js                # UI 管理器
│   └── api调用测试/             # API 测试示例
└── README.md                    # 项目文档
```

## 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 不需要（纯前端项目）
- **浏览器**: 现代浏览器（Chrome、Firefox、Safari、Edge）

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd GuideBot-main/项目
```

### 2. 配置后端环境

进入后端目录并安装依赖：

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

复制并编辑 `.env` 文件：

```env
# 阿里云 DashScope API 密钥
DASHSCOPE_API_KEY=your_api_key_here

# 使用的模型
DASHSCOPE_MODEL=qwen-vl-max

# 视觉模型
DASHSCOPE_VISION_MODEL=qwen-vl-max

# 是否允许 AI 失败时使用回退数据
AI_ALLOW_MOCK_FALLBACK=false

# AI 推理努力程度 (low/medium/high)
AI_REASONING_EFFORT=high

# 指引风格 (friendly_detailed/concise/expert)
AI_GUIDE_STYLE=friendly_detailed

# 温度参数
AI_TEMPERATURE=0.35

# 最大生成 token 数
AI_MAX_TOKENS=1800

# 思考预算
AI_THINKING_BUDGET=2048

# 请求超时时间（秒）
AI_REQUEST_TIMEOUT=75
```

**获取 API Key**：
1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建 API Key
4. 将 API Key 填入 `.env` 文件

### 4. 启动后端服务

```bash
cd backend
python app.py
```

后端服务将在 `http://localhost:5000` 启动。

### 5. 启动前端服务

#### 方式一：直接打开

直接在浏览器中打开 `frontend/index.html` 文件。

#### 方式二：使用本地服务器（推荐）

使用 Python 启动简单的 HTTP 服务器：

```bash
cd frontend
python -m http.server 8000
```

然后在浏览器中访问 `http://localhost:8000`。

## API 接口文档

### 健康检查

**接口**: `GET /api/health`

**响应示例**:
```json
{
  "status": "healthy",
  "service": "GuideBot Backend",
  "version": "1.2.0",
  "build": "2026-03-09-ai-unified-url-text",
  "ai": {
    "ready": true,
    "allow_mock_fallback": false,
    "error": null
  },
  "endpoints": [
    "/api/health",
    "/api/process/image",
    "/api/process/url",
    "/api/process/text",
    "/api/community/guides",
    "/api/community/share",
    "/api/test/ai"
  ]
}
```

### 处理图片

**接口**: `POST /api/process/image`

**请求参数**:
```json
{
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "note": "我想在这个页面完成支付，下一步点哪里？"
}
```

**响应示例**:
```json
{
  "success": true,
  "steps": [
    {
      "step": 1,
      "title": "点击登录按钮",
      "description": "点击页面右上角的登录按钮，进入登录流程。",
      "purpose": "进入登录页面",
      "expected_result": "页面跳转到登录界面",
      "tip": "确保网络连接稳定",
      "warning": "不要多次点击",
      "rect": {"x": 650, "y": 50, "width": 100, "height": 40},
      "color": "#ff0000"
    }
  ],
  "title": "登录操作指南",
  "summary": "本指南将帮助您完成登录操作",
  "estimated_time": "约3分钟",
  "difficulty": "初级",
  "prerequisites": ["准备好账号信息"],
  "common_mistakes": ["输入错误的密码"],
  "final_check": ["成功登录"],
  "image": "data:image/png;base64,...",
  "message": "图片分析完成。",
  "ai_used": true,
  "source": "ai"
}
```

### 处理网址

**接口**: `POST /api/process/url`

**请求参数**:
```json
{
  "url": "https://example.com"
}
```

**响应示例**:
```json
{
  "success": true,
  "steps": [...],
  "title": "网站使用指南",
  "summary": "...",
  "estimated_time": "约5分钟",
  "difficulty": "初级",
  "prerequisites": [...],
  "common_mistakes": [...],
  "final_check": [...],
  "url": "https://example.com",
  "message": "网址处理完成。",
  "ai_used": true,
  "source": "ai"
}
```

### 处理文本

**接口**: `POST /api/process/text`

**请求参数**:
```json
{
  "text": "微信怎么发朋友圈"
}
```

**响应示例**:
```json
{
  "success": true,
  "steps": [...],
  "title": "微信发朋友圈指南",
  "summary": "...",
  "estimated_time": "约2分钟",
  "difficulty": "初级",
  "prerequisites": [...],
  "common_mistakes": [...],
  "final_check": [...],
  "text": "微信怎么发朋友圈",
  "scenario": "general",
  "message": "文本处理完成。",
  "ai_used": true,
  "source": "ai"
}
```

### 获取社区指南

**接口**: `GET /api/community/guides`

**响应示例**:
```json
{
  "success": true,
  "guides": [
    {
      "id": 1,
      "title": "WeChat Moments Quick Guide",
      "author": "UserA",
      "likes": 42,
      "steps": 3,
      "created_at": "2026-01-15",
      "scenario": "social"
    }
  ],
  "total": 1,
  "message": "Community guides."
}
```

### 分享到社区

**接口**: `POST /api/community/share`

**请求参数**:
```json
{
  "title": "操作指南标题",
  "steps": [...]
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "Shared successfully.",
  "share_id": "abc123..."
}
```

## 使用指南

### 截图上传模式

1. 点击"选择截图文件"按钮或直接拖拽图片到上传区域
2. （可选）在备注框中补充你的问题
3. 点击"生成指引"按钮
4. 等待 AI 分析并生成操作步骤
5. 查看生成的详细指引

### 网址输入模式

1. 切换到"网址输入"标签页
2. 输入目标网址
3. 点击"生成指引"按钮
4. 查看生成的网站使用教程

### 文本描述模式

1. 切换到"文本描述"标签页
2. 输入你的目标任务描述
3. 点击"生成指引"按钮
4. 查看生成的操作指引

## 部署说明

### 开发环境部署

按照"快速开始"章节的步骤操作即可。

### 生产环境部署

#### 后端部署

推荐使用 Gunicorn 或 uWSGI 部署 Flask 应用：

```bash
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 前端部署

将 `frontend` 目录部署到任何静态文件服务器：
- Nginx
- Apache
- Vercel
- Netlify
- GitHub Pages

#### 使用 Docker 部署（可选）

创建 `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建并运行：

```bash
docker build -t guidebot-backend .
docker run -p 5000:5000 --env-file backend/.env guidebot-backend
```

## 配置说明

### AI 模型参数

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `DASHSCOPE_MODEL` | 主模型名称 | qwen-vl-max | qwen-vl-max, qwen-max 等 |
| `DASHSCOPE_VISION_MODEL` | 视觉模型名称 | qwen-vl-max | qwen-vl-max, qwen-vl-max-latest 等 |
| `AI_TEMPERATURE` | 生成温度 | 0.35 | 0.0-1.0 |
| `AI_MAX_TOKENS` | 最大生成 token 数 | 1800 | 1-4096 |
| `AI_REASONING_EFFORT` | 推理努力程度 | high | low, medium, high |
| `AI_THINKING_BUDGET` | 思考预算 | 2048 | 0-8192 |
| `AI_GUIDE_STYLE` | 指引风格 | friendly_detailed | friendly_detailed, concise, expert |

### 指引风格说明

- **friendly_detailed**：友好详细，适合新手，步骤详尽
- **concise**：简洁专业，适合有经验的用户
- **expert**：专家级，强调判断标准和风险提示

## 常见问题

### 1. AI 服务不可用

**问题**：提示"AI 服务不可用"

**解决方案**：
- 检查 `.env` 文件中的 `DASHSCOPE_API_KEY` 是否正确
- 确认 API Key 是否有足够的配额
- 检查网络连接是否正常
- 查看后端日志获取详细错误信息

### 2. 生成的步骤不准确

**问题**：AI 生成的步骤与截图不匹配

**解决方案**：
- 确保截图清晰，包含完整的界面元素
- 在备注中提供更具体的问题描述
- 尝试调整 `AI_GUIDE_STYLE` 参数
- 使用更高质量的截图

### 3. 响应速度慢

**问题**：生成指引需要较长时间

**解决方案**：
- 检查网络连接速度
- 调整 `AI_MAX_TOKENS` 参数（降低可加快速度）
- 调整 `AI_REASONING_EFFORT` 为 `low` 或 `medium`

### 4. 跨域问题

**问题**：前端无法连接后端 API

**解决方案**：
- 确保后端已启动并运行在正确端口
- 检查 CORS 配置
- 如果使用不同域名，需要配置正确的 CORS 策略

## 技术亮点

1. **智能场景分析**：自动识别不同类型的界面和场景
2. **图像锚定验证**：确保生成的步骤基于截图中的可见元素
3. **自动质量控制**：检测模板化输出并自动重试
4. **多模态支持**：支持图片、网址、文本三种输入方式
5. **用户友好界面**：现代化的 UI 设计，支持拖拽上传
6. **灵活配置**：丰富的配置选项，适应不同使用场景

## 开发计划

- [ ] 支持更多 AI 模型（如 GPT-4V、Claude 3 等）
- [ ] 添加用户认证和个性化配置
- [ ] 实现指南的保存和分享功能
- [ ] 支持批量处理多个截图
- [ ] 添加指南导出功能（PDF、Word 等）
- [ ] 实现社区指南库和评分系统
- [ ] 支持多语言界面

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 加入讨论组

## 致谢

感谢阿里云 DashScope 提供强大的 AI 能力支持！

---

**注意**：本项目仅供学习和研究使用。请遵守相关法律法规和 API 使用条款。
