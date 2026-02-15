// API基础配置
const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000/api' 
    : 'https://your-backend.vercel.app/api'

// 上传图片处理
async function uploadImage(file) {
    const formData = new FormData()
    formData.append('image', file)
    
    const response = await fetch(`${API_BASE}/process/image`, {
        method: 'POST',
        body: formData
    })
    
    if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
    }
    
    return await response.json()
}

// 处理网址
async function processUrlAPI(url) {
    const response = await fetch(`${API_BASE}/process/url`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    
    if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
    }
    
    return await response.json()
}

// 处理文本
async function processTextAPI(text) {
    const response = await fetch(`${API_BASE}/process/text`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    })
    
    if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
    }
    
    return await response.json()
}

// 健康检查
async function healthCheck() {
    const response = await fetch(`${API_BASE}/health`)
    return await response.json()
}