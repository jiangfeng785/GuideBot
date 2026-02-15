// UI管理模块
const UIManager = {
    // 显示输入区域
    showInputSection() {
        document.getElementById('input-section').style.display = 'block'
        document.getElementById('result-section').style.display = 'none'
    },

    // 显示结果区域
    showResultSection() {
        document.getElementById('input-section').style.display = 'none'
        document.getElementById('result-section').style.display = 'block'
    },

    // 显示加载状态
    showLoading() {
        document.getElementById('loading').style.display = 'block'
    },

    // 隐藏加载状态
    hideLoading() {
        document.getElementById('loading').style.display = 'none'
    },

    // 切换标签页
    switchTab(tabName) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'))
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'))
        
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active')
        document.getElementById(`${tabName}-tab`).classList.add('active')
    },

    // 显示图片预览
    showImagePreview(imageSrc) {
        const preview = document.getElementById('image-preview')
        preview.innerHTML = `
            <div class="preview-container">
                <img src="${imageSrc}" alt="预览图" style="max-width: 400px; max-height: 300px;">
                <button class="delete-image-btn" id="delete-image-btn">删除图片</button>
            </div>
        `
        
        // 绑定删除按钮事件
        document.getElementById('delete-image-btn').addEventListener('click', this.deleteImage)
    },

    // 删除图片
    deleteImage() {
        const preview = document.getElementById('image-preview')
        preview.innerHTML = ''
        
        // 清除文件输入
        const fileInput = document.getElementById('file-input')
        fileInput.value = ''
        
        // 清除当前文件
        window.currentFile = null
    },

    // 显示结果步骤
    displaySteps(steps) {
        const stepsContainer = document.getElementById('steps-container')
        stepsContainer.innerHTML = ''
        
        if (steps && steps.length > 0) {
            steps.forEach(step => {
                const stepElement = this.createStepElement(step)
                stepsContainer.appendChild(stepElement)
            })
        } else {
            stepsContainer.innerHTML = '<p>生成指引失败</p>'
        }
    },

    // 创建步骤元素
    createStepElement(step) {
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
    },

    // 显示错误信息
    showError(message) {
        alert(message)
    },

    // 重置表单
    resetForm() {
        document.getElementById('url-input').value = ''
        document.getElementById('text-input').value = ''
        this.deleteImage()
    }
}

// 导出UI管理器（如果使用模块化）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIManager
}
