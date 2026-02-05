// Canvas绘制工具
function drawStepCanvas(step, canvasId) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    
    // 设置Canvas尺寸
    canvas.width = 800
    canvas.height = 600
    
    // 绘制背景（灰色）
    ctx.fillStyle = '#f0f0f0'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    // 绘制标注框
    if (step.rect) {
        // 绘制红色边框
        ctx.strokeStyle = '#ff0000'
        ctx.lineWidth = 3
        ctx.strokeRect(step.rect.x, step.rect.y, step.rect.width, step.rect.height)
        
        // 绘制步骤编号
        ctx.fillStyle = '#ff0000'
        ctx.font = 'bold 20px Arial'
        ctx.fillText(step.step.toString(), step.rect.x + 5, step.rect.y + 20)
        
        // 绘制描述文字
        ctx.fillStyle = '#000000'
        ctx.font = '14px Arial'
        ctx.fillText(step.description, step.rect.x, step.rect.y + step.rect.height + 20)
    }
}

// 下载Canvas图片
function downloadCanvas(canvasId, filename) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return
    
    const link = document.createElement('a')
    link.download = filename || 'guide-step.png'
    link.href = canvas.toDataURL()
    link.click()
}