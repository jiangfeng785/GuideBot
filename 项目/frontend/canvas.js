// Canvas drawing utility
function drawStepCanvas(step, canvasId) {
    const canvas = document.getElementById(canvasId)
    if (!canvas || typeof canvas.getContext !== 'function') return

    const ctx = canvas.getContext('2d')

    canvas.width = 800
    canvas.height = 600

    ctx.fillStyle = '#f0f0f0'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    if (!step || !step.rect) return

    const rect = step.rect
    const x = Number(rect.x) || 0
    const y = Number(rect.y) || 0
    const width = Number(rect.width) || 120
    const height = Number(rect.height) || 40

    const color = step.color || '#ff0000'

    ctx.strokeStyle = color
    ctx.lineWidth = 3
    ctx.strokeRect(x, y, width, height)

    ctx.fillStyle = color
    ctx.font = 'bold 20px Arial'
    ctx.fillText(String(step.step || ''), x + 6, y + 22)

    ctx.fillStyle = '#000000'
    ctx.font = '14px Arial'
    ctx.fillText(step.description || '', x, y + height + 20)
}

function downloadCanvas(canvasId, filename) {
    const canvas = document.getElementById(canvasId)
    if (!canvas) return

    const link = document.createElement('a')
    link.download = filename || 'guide-step.png'
    link.href = canvas.toDataURL()
    link.click()
}
