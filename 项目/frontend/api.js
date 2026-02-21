// API base config
const isLocalHost = ['localhost', '127.0.0.1', ''].includes(window.location.hostname)
const API_BASE = isLocalHost
    ? 'http://localhost:5000/api'
    : 'https://your-backend.vercel.app/api'

// Upload image and process
async function uploadImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = function (e) {
            const base64Data = e.target.result

            fetch(`${API_BASE}/process/image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: base64Data }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP错误: ${response.status}`)
                    }
                    return response.json()
                })
                .then(data => resolve(data))
                .catch(error => reject(error))
        }

        reader.onerror = function () {
            reject(new Error('文件读取失败'))
        }

        reader.readAsDataURL(file)
    })
}

async function processUrlAPI(url) {
    const response = await fetch(`${API_BASE}/process/url`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
    })

    if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
    }

    return await response.json()
}

async function processTextAPI(text) {
    const response = await fetch(`${API_BASE}/process/text`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    })

    if (!response.ok) {
        throw new Error(`HTTP错误: ${response.status}`)
    }

    return await response.json()
}

async function healthCheck() {
    const response = await fetch(`${API_BASE}/health`)
    return await response.json()
}
