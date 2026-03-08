// UI manager
const UIManager = {
    _loadingTimer: null,
    _loadingTipTimer: null,

    showInputSection() {
        document.getElementById('input-section').style.display = 'block'
        document.getElementById('result-section').style.display = 'none'
    },

    showResultSection() {
        document.getElementById('input-section').style.display = 'none'
        document.getElementById('result-section').style.display = 'block'
    },

    showLoading() {
        const loading = document.getElementById('loading')
        if (!loading) return

        loading.innerHTML = `
            <div class="ai-loading">
                <div class="ai-loading-orb"></div>
                <p class="ai-loading-title">AI 正在思考<span id="loading-dots">.</span></p>
                <p class="ai-loading-tip" id="loading-tip">正在理解你的任务目标...</p>
            </div>
        `
        loading.style.display = 'block'

        const dotsEl = document.getElementById('loading-dots')
        let dotCount = 1
        this._loadingTimer = window.setInterval(() => {
            dotCount = (dotCount % 3) + 1
            if (dotsEl) dotsEl.textContent = '.'.repeat(dotCount)
        }, 380)

        const tips = [
            '正在理解你的任务目标...',
            '正在规划更清晰的步骤结构...',
            '正在补充避坑提醒与完成检查...',
            '正在润色为亲和版表达...',
        ]
        const tipEl = document.getElementById('loading-tip')
        let tipIndex = 0
        this._loadingTipTimer = window.setInterval(() => {
            tipIndex = (tipIndex + 1) % tips.length
            if (tipEl) tipEl.textContent = tips[tipIndex]
        }, 1600)
    },

    hideLoading() {
        if (this._loadingTimer) {
            clearInterval(this._loadingTimer)
            this._loadingTimer = null
        }
        if (this._loadingTipTimer) {
            clearInterval(this._loadingTipTimer)
            this._loadingTipTimer = null
        }
        const loading = document.getElementById('loading')
        if (loading) {
            loading.style.display = 'none'
            loading.innerHTML = ''
        }
    },

    switchTab(tabName) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'))
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'))

        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active')
        document.getElementById(`${tabName}-tab`).classList.add('active')
    },

    showImagePreview(imageSrc) {
        const preview = document.getElementById('image-preview')
        preview.innerHTML = `
            <div class="preview-container">
                <img src="${imageSrc}" alt="Preview" style="max-width: 400px; max-height: 300px;">
                <button class="delete-image-btn" id="delete-image-btn">删除图片</button>
            </div>
        `

        document.getElementById('delete-image-btn').addEventListener('click', this.deleteImage)
    },

    deleteImage() {
        const preview = document.getElementById('image-preview')
        preview.innerHTML = ''

        const fileInput = document.getElementById('file-input')
        fileInput.value = ''

        window.currentFile = null
    },

    displayTextGuide(result) {
        const stepsContainer = document.getElementById('steps-container')
        stepsContainer.innerHTML = ''

        const steps = Array.isArray(result && result.steps) ? result.steps : []
        if (!steps.length) {
            const errorText = (result && result.error) ? result.error : '未生成任何说明内容'
            stepsContainer.innerHTML = `<p class="guide-empty">${errorText}</p>`
            return
        }

        const wrapper = document.createElement('article')
        wrapper.className = 'guide-doc'

        const title = document.createElement('h3')
        title.className = 'guide-title'
        title.textContent = (result && result.title) ? result.title : '操作说明'
        wrapper.appendChild(title)

        const metaBar = document.createElement('div')
        metaBar.className = 'guide-badges'
        const metaValues = [
            `来源：${result && result.ai_used ? 'AI生成' : '回退说明'}`,
            `难度：${(result && result.difficulty) ? result.difficulty : '初级'}`,
            `预计耗时：${(result && result.estimated_time) ? result.estimated_time : '约3分钟'}`,
        ]
        metaValues.forEach(text => {
            const badge = document.createElement('span')
            badge.className = 'guide-badge'
            badge.textContent = text
            metaBar.appendChild(badge)
        })
        wrapper.appendChild(metaBar)

        const summaryText = (result && result.summary) ? result.summary : (result && result.message)
        if (summaryText) {
            const summary = document.createElement('p')
            summary.className = 'guide-summary'
            summary.textContent = summaryText
            wrapper.appendChild(summary)
        }

        this.appendStringListSection(wrapper, '准备事项', result && result.prerequisites, 'guide-list')

        const stepsTitle = document.createElement('h4')
        stepsTitle.className = 'guide-section-title'
        stepsTitle.textContent = '操作步骤'
        wrapper.appendChild(stepsTitle)

        const list = document.createElement('ol')
        list.className = 'guide-steps'
        steps.forEach((step, idx) => {
            const safeStep = {
                ...step,
                step: Number.isInteger(step.step) ? step.step : idx + 1,
                description: step.description || `步骤 ${idx + 1}`,
            }

            const item = document.createElement('li')
            item.className = 'guide-step-card'

            const stepHeader = document.createElement('h5')
            stepHeader.className = 'guide-step-title'
            stepHeader.textContent = `第 ${safeStep.step} 步：${step.title || safeStep.description}`
            item.appendChild(stepHeader)

            const desc = document.createElement('p')
            desc.className = 'guide-step-desc'
            desc.textContent = safeStep.description
            item.appendChild(desc)

            if (step && step.purpose) {
                const purpose = document.createElement('p')
                purpose.className = 'guide-detail'
                purpose.textContent = `目的：${step.purpose}`
                item.appendChild(purpose)
            }

            if (step && step.expected_result) {
                const expected = document.createElement('p')
                expected.className = 'guide-detail'
                expected.textContent = `预期结果：${step.expected_result}`
                item.appendChild(expected)
            }

            if (step && step.tip) {
                const tip = document.createElement('p')
                tip.className = 'guide-tip'
                tip.textContent = `提示：${step.tip}`
                item.appendChild(tip)
            }

            if (step && step.warning) {
                const warning = document.createElement('p')
                warning.className = 'guide-warning'
                warning.textContent = `注意：${step.warning}`
                item.appendChild(warning)
            }

            list.appendChild(item)
        })

        wrapper.appendChild(list)
        this.appendStringListSection(wrapper, '常见错误', result && result.common_mistakes, 'guide-list guide-danger')
        this.appendStringListSection(wrapper, '完成检查', result && result.final_check, 'guide-list guide-check')
        stepsContainer.appendChild(wrapper)
    },

    appendStringListSection(wrapper, titleText, items, className) {
        const values = Array.isArray(items) ? items.filter(v => typeof v === 'string' && v.trim()) : []
        if (!values.length) {
            return
        }

        const title = document.createElement('h4')
        title.className = 'guide-section-title'
        title.textContent = titleText
        wrapper.appendChild(title)

        const list = document.createElement('ul')
        list.className = className
        values.forEach(text => {
            const li = document.createElement('li')
            li.textContent = text
            list.appendChild(li)
        })
        wrapper.appendChild(list)
    },

    showError(message) {
        alert(message)
    },

    resetForm() {
        document.getElementById('url-input').value = ''
        document.getElementById('text-input').value = ''
        this.deleteImage()
    },
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIManager
}
