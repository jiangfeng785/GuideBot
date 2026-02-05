// 主应用入口
document.addEventListener('DOMContentLoaded', function() {
    console.log('GuideBot应用启动成功')
    
    // 初始化应用
    initApp()
})

function initApp() {
    // 绑定事件监听器
    bindEvents()
}

function bindEvents() {
    // 标签页切换
    const tabBtns = document.querySelectorAll('.tab-btn')
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.dataset.tab
            switchTab(tabName)
        })
    })
    
    // 文件选择
    document.getElementById('select-file-btn').addEventListener('click', function() {
        document.getElementById('file-input').click()
    })
    
    // 文件输入变化
    document.getElementById('file-input').addEventListener('change', handleFileSelect)
    
    // 拖拽上传
    const uploadArea = document.getElementById('upload-area')
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault()
        this.classList.add('drag-over')
    })
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault()
        this.classList.remove('drag-over')
    })
    uploadArea.addEventListener('drop', handleFileDrop)
    
    // 提交按钮
    document.getElementById('submit-btn').addEventListener('click', handleSubmit)
    
    // 返回按钮
    document.getElementById('back-btn').addEventListener('click', function() {
        showInputSection()
    })
}

// 切换标签页
function switchTab(tabName) {
    // 移除所有active类
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'))
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'))
    
    // 添加active类到当前标签
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active')
    document.getElementById(`${tabName}-tab`).classList.add('active')
}

// 处理文件选择
function handleFileSelect(event) {
    const file = event.target.files[0]
    if (file) {
        handleFile(file)
    }
}

// 处理拖拽文件
function handleFileDrop(event) {
    event.preventDefault()
    const uploadArea = document.getElementById('upload-area')
    uploadArea.classList.remove('drag-over')
    
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
        handleFile(file)
    } else {
        alert('请上传图片文件')
    }
}

// 处理文件
function handleFile(file) {
    // 显示预览
    const reader = new FileReader()
    reader.onload = function(e) {
        const preview = document.getElementById('image-preview')
        preview.innerHTML = `<img src="${e.target.result}" alt="预览图" style="max-width: 400px; max-height: 300px;">`
    }
    reader.readAsDataURL(file)
    
    // 存储当前文件
    window.currentFile = file
}

// 处理提交
function handleSubmit() {
    const activeTab = document.querySelector('.tab-btn.active').dataset.tab
    
    if (activeTab === 'screenshot') {
        if (!window.currentFile) {
            alert('请先选择截图文件')
            return
        }
        processImage(window.currentFile)
    } else if (activeTab === 'url') {
        const url = document.getElementById('url-input').value.trim()
        if (!url) {
            alert('请输入网址')
            return
        }
        processUrl(url)
    } else if (activeTab === 'text') {
        const text = document.getElementById('text-input').value.trim()
        if (!text) {
            alert('请输入文本描述')
            return
        }
        processText(text)
    }
}

// 处理图片
async function processImage(file) {
    showLoading()
    
    try {
        const result = await uploadImage(file)
        displayResult(result)
    } catch (error) {
        alert('处理失败：' + error.message)
        hideLoading()
    }
}

// 处理网址
async function processUrl(url) {
    showLoading()
    
    try {
        const result = await processUrlAPI(url)
        displayResult(result)
    } catch (error) {
        alert('处理失败：' + error.message)
        hideLoading()
    }
}

// 处理文本
async function processText(text) {
    showLoading()
    
    try {
        const result = await processTextAPI(text)
        displayResult(result)
    } catch (error) {
        alert('处理失败：' + error.message)
        hideLoading()
    }
}

// 显示结果
function displayResult(result) {
    hideLoading()
    showResultSection()
    
    const stepsContainer = document.getElementById('steps-container')
    stepsContainer.innerHTML = ''
    
    if (result.success && result.steps) {
        result.steps.forEach(step => {
            const stepElement = createStepElement(step)
            stepsContainer.appendChild(stepElement)
        })
    } else {
        stepsContainer.innerHTML = '<p>生成指引失败</p>'
    }
}

// 创建步骤元素
function createStepElement(step) {
    const div = document.createElement('div')
    div.className = 'step'
    div.innerHTML = `
        <h3>第${step.step}步：${step.description}</h3>
        <div class="step-canvas" id="canvas-${step.step}"></div>
    `
    
    // 延迟绘制Canvas（等DOM渲染完成）
    setTimeout(() => {
        drawStepCanvas(step, `canvas-${step.step}`)
    }, 100)
    
    return div
}

// 显示/隐藏部分
function showInputSection() {
    document.getElementById('input-section').style.display = 'block'
    document.getElementById('result-section').style.display = 'none'
}

function showResultSection() {
    document.getElementById('input-section').style.display = 'none'
    document.getElementById('result-section').style.display = 'block'
}

function showLoading() {
    document.getElementById('loading').style.display = 'block'
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none'
}