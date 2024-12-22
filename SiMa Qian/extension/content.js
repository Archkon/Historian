let tooltip = null;
let highlightedText = null;

// 创建工具提示
function createTooltip(text, x, y) {
    removeTooltip();
    
    tooltip = document.createElement('div');
    tooltip.className = 'sima-tooltip';
    tooltip.style.left = `${x}px`;
    tooltip.style.top = `${y}px`;
    
    const content = document.createElement('div');
    content.textContent = text;
    tooltip.appendChild(content);
    
    const actions = document.createElement('div');
    actions.className = 'sima-tooltip-actions';
    
    const analyzeBtn = document.createElement('button');
    analyzeBtn.className = 'sima-tooltip-button';
    analyzeBtn.textContent = '分析';
    analyzeBtn.onclick = () => analyzeText(text);
    
    const translateBtn = document.createElement('button');
    translateBtn.className = 'sima-tooltip-button';
    translateBtn.textContent = '翻译';
    translateBtn.onclick = () => translateText(text);
    
    actions.appendChild(analyzeBtn);
    actions.appendChild(translateBtn);
    tooltip.appendChild(actions);
    
    document.body.appendChild(tooltip);
}

// 移除工具提示
function removeTooltip() {
    if (tooltip) {
        tooltip.remove();
        tooltip = null;
    }
}

// 高亮选中的文本
function highlightSelection() {
    if (highlightedText) {
        highlightedText.outerHTML = highlightedText.innerHTML;
        highlightedText = null;
    }
    
    const selection = window.getSelection();
    if (!selection.rangeCount) return;
    
    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.className = 'sima-highlight';
    range.surroundContents(span);
    highlightedText = span;
}

// 分析文本
async function analyzeText(text) {
    try {
        chrome.runtime.sendMessage({
            type: 'process',
            action: 'analyze',
            text: text
        }, response => {
            if (response.status === 'success') {
                updateTooltipContent(response.message);
            } else {
                updateTooltipContent('分析失败，请重试');
            }
        });
    } catch (error) {
        console.error('分析错误:', error);
        updateTooltipContent('分析出错，请稍后重试');
    }
}

// 翻译文本
async function translateText(text) {
    try {
        chrome.runtime.sendMessage({
            type: 'process',
            action: 'translate',
            text: text
        }, response => {
            if (response.status === 'success') {
                updateTooltipContent(response.message);
            } else {
                updateTooltipContent('翻译失败，请重试');
            }
        });
    } catch (error) {
        console.error('翻译错误:', error);
        updateTooltipContent('翻译出错，请稍后重试');
    }
}

// 更新工具提示内容
function updateTooltipContent(message) {
    if (tooltip) {
        const content = tooltip.querySelector('div');
        content.textContent = message;
    }
}

// 监听选中文本事件
document.addEventListener('mouseup', function(e) {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
        highlightSelection();
        createTooltip(selectedText, e.pageX, e.pageY);
    } else {
        removeTooltip();
    }
});

// 点击其他地方时移除工具提示
document.addEventListener('mousedown', function(e) {
    if (tooltip && !tooltip.contains(e.target)) {
        removeTooltip();
    }
}); 