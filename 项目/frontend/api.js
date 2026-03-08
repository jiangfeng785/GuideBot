// API base config
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
const host = window.location.hostname || 'localhost'
const isPrivateHost =
    host === 'localhost' ||
    host === '127.0.0.1' ||
    host === '::1' ||
    /^192\.168\.\d{1,3}\.\d{1,3}$/.test(host) ||
    /^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(host) ||
    /^172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}$/.test(host)

const API_BASE = isPrivateHost
    ? `http://${host === '::1' ? 'localhost' : host}:5000/api`
    : 'https://your-backend.vercel.app/api'
// Upload image and process
async function uploadImage(file, note = '') {
<<<<<<< HEAD
=======
const isLocalHost = ['localhost', '127.0.0.1', ''].includes(window.location.hostname)
const API_BASE = isLocalHost
    ? 'http://localhost:5000/api'
    : 'https://your-backend.vercel.app/api'

// Upload image and process
async function uploadImage(file) {
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = function (e) {
            const base64Data = e.target.result

            fetch(`${API_BASE}/process/image`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
<<<<<<< HEAD
<<<<<<< HEAD
                body: JSON.stringify({ image: base64Data, note }),
=======
                body: JSON.stringify({ image: base64Data }),
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======
                body: JSON.stringify({ image: base64Data, note }),
>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
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
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
=======

>>>>>>> 19b38e4b16ab2fde41dfdc244fe024ad7bb62b76
