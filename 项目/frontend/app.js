<<<<<<< HEAD
﻿document.addEventListener('DOMContentLoaded', () => {
    bindEvents()
})

let latestRequestId = 0

function bindEvents() {
    // Tab 切换
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            UIManager.switchTab(this.dataset.tab)
        })
    })

    // 文件选择
=======
﻿// App entry

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

>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
    document.getElementById('select-file-btn').addEventListener('click', () => {
        document.getElementById('file-input').click()
    })

<<<<<<< HEAD
    document.getElementById('file-input').addEventListener('change', (e) => {
        const file = e.target.files[0]
        if (file) handleFile(file)
    })

    // 拖拽上传
    const uploadArea = document.getElementById('upload-area')
    uploadArea.addEventListener('dragover', e => { e.preventDefault(); uploadArea.style.borderColor = 'var(--primary-color)' })
    uploadArea.addEventListener('dragleave', e => { e.preventDefault(); uploadArea.style.borderColor = '' })
    uploadArea.addEventListener('drop', e => {
        e.preventDefault()
        const file = e.dataTransfer.files[0]
        if (file) handleFile(file)
    })

    // 提交按钮
    document.getElementById('submit-btn').addEventListener('click', handleSubmit)

    // 返回按钮
    document.getElementById('back-btn').addEventListener('click', () => UIManager.showInputSection())
}

function handleFile(file) {
    const reader = new FileReader()
    reader.onload = (e) => UIManager.showImagePreview(e.target.result)
    reader.readAsDataURL(file)
    window.selectedFile = file
}

async function handleSubmit() {
    const requestId = ++latestRequestId
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab
    UIManager.showResultSection()
    UIManager.prepareForNewResult()
    UIManager.showLoading()
    setSubmitLoading(true)

    try {
        let result
        if (activeTab === 'screenshot' && window.selectedFile) {
            const note = (document.getElementById('screenshot-note')?.value || '').trim()
            result = await uploadImage(window.selectedFile, note)
        } else if (activeTab === 'url') {
            const url = document.getElementById('url-input').value
            result = await processUrlAPI(url)
        } else {
            const text = document.getElementById('text-input').value
            result = await processTextAPI(text)
        }

        if (requestId !== latestRequestId) {
            return
        }

        UIManager.hideLoading()
        UIManager.displayTextGuide(result)
    } catch (err) {
        if (requestId !== latestRequestId) {
            return
        }
        UIManager.hideLoading()
        UIManager.showError('生成失败: ' + err.message)
    } finally {
        if (requestId === latestRequestId) {
            setSubmitLoading(false)
        }
    }
}

function setSubmitLoading(isLoading) {
    const submitBtn = document.getElementById('submit-btn')
    if (!submitBtn) {
        return
    }
    submitBtn.disabled = isLoading
    submitBtn.textContent = isLoading ? '生成中...' : '生成指引'
=======
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
>>>>>>> 6587051b175b699b6cc75260a41b0cfc88afc1bd
}
