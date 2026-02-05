// API基础地址
const API_BASE = 'http://localhost:5000/api'

// 显示结果到页面
function showResult(data) {
    const resultDiv = document.getElementById('result')
    resultDiv.textContent = JSON.stringify(data, null, 2)
}

// 测试后端连接
async function testHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`)
        const data = await response.json()
        showResult(data)
    } catch (error) {
        showResult({ error: '连接失败: ' + error.message })
    }
}

// 测试图片处理
async function testProcessImage() {
    try {
        // 创建一个虚拟的图片文件用于测试
        const canvas = document.createElement('canvas')
        canvas.width = 100
        canvas.height = 100
        const ctx = canvas.getContext('2d')
        
        // 在Canvas上画点东西
        ctx.fillStyle = '#f0f0f0'
        ctx.fillRect(0, 0, 100, 100)
        ctx.fillStyle = '#007bff'
        ctx.fillRect(20, 20, 60, 60)
        
        // 将Canvas转为Blob
        const blob = await new Promise(resolve => {
            canvas.toBlob(resolve, 'image/png')
        })
        
        // 创建FormData并上传
        const formData = new FormData()
        formData.append('image', blob, 'test.png')
        
        const response = await fetch(`${API_BASE}/process/image`, {
            method: 'POST',
            body: formData
        })
        
        const data = await response.json()
        showResult(data)
        
    } catch (error) {
        showResult({ error: '处理失败: ' + error.message })
    }
}