// App entry

document.addEventListener('DOMContentLoaded', () => {
    initApp()
})

function initApp() {
    bindEvents()
}

function bindEvents() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            switchTab(this.dataset.tab)
        })
    })

    document.getElementById('select-file-btn').addEventListener('click', () => {
        document.getElementById('file-input').click()
    })

    document.getElementById('file-input').addEventListener('change', handleFileSelect)

    const uploadArea = document.getElementById('upload-area')
    uploadArea.addEventListener('dragover', e => {
        e.preventDefault()
        uploadArea.classList.add('drag-over')
    })

    uploadArea.addEventListener('dragleave', e => {
        e.preventDefault()
        uploadArea.classList.remove('drag-over')
    })

    uploadArea.addEventListener('drop', handleFileDrop)

    document.getElementById('submit-btn').addEventListener('click', handleSubmit)
    document.getElementById('back-btn').addEventListener('click', () => UIManager.showInputSection())
}

function switchTab(tabName) {
    UIManager.switchTab(tabName)
}

function handleFileSelect(event) {
    const file = event.target.files && event.target.files[0]
    if (file) {
        handleFile(file)
    }
}

function handleFileDrop(event) {
    event.preventDefault()
    const uploadArea = document.getElementById('upload-area')
    uploadArea.classList.remove('drag-over')

    const file = event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0]
    if (!file || !file.type.startsWith('image/')) {
        alert('请上传图片文件')
        return
    }

    handleFile(file)
}

function handleFile(file) {
    const reader = new FileReader()
    reader.onload = e => {
        UIManager.showImagePreview(e.target.result)
    }
    reader.readAsDataURL(file)

    window.currentFile = file
}

function handleSubmit() {
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab

    if (activeTab === 'screenshot') {
        if (!window.currentFile) {
            alert('请先选择截图文件')
            return
        }
        processImage(window.currentFile)
        return
    }

    if (activeTab === 'url') {
        const url = document.getElementById('url-input').value.trim()
        if (!url) {
            alert('请输入网址')
            return
        }
        processUrl(url)
        return
    }

    if (activeTab === 'text') {
        const text = document.getElementById('text-input').value.trim()
        if (!text) {
            alert('请输入文本描述')
            return
        }
        processText(text)
    }
}

async function processImage(file) {
    UIManager.showLoading()
    try {
        const result = await uploadImage(file)
        displayResult(result)
    } catch (error) {
        UIManager.hideLoading()
        UIManager.showError(`处理失败: ${error.message}`)
    }
}

async function processUrl(url) {
    UIManager.showLoading()
    try {
        const result = await processUrlAPI(url)
        displayResult(result)
    } catch (error) {
        UIManager.hideLoading()
        UIManager.showError(`处理失败: ${error.message}`)
    }
}

async function processText(text) {
    UIManager.showLoading()
    try {
        const result = await processTextAPI(text)
        displayResult(result)
    } catch (error) {
        UIManager.hideLoading()
        UIManager.showError(`处理失败: ${error.message}`)
    }
}

function displayResult(result) {
    UIManager.hideLoading()
    UIManager.showResultSection()

    if (!result || !result.success) {
        UIManager.displayTextGuide(result || {})
        if (result && result.error) {
            UIManager.showError(result.error)
        }
        return
    }

    UIManager.displayTextGuide(result)
}
