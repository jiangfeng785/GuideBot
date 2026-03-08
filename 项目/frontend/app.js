document.addEventListener('DOMContentLoaded', () => {
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
    document.getElementById('select-file-btn').addEventListener('click', () => {
        document.getElementById('file-input').click()
    })

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
}
