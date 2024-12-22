// 扩展安装时的初始化
chrome.runtime.onInstalled.addListener(() => {
    console.log('史记助手已安装');
    
    // 创建右键菜单
    chrome.contextMenus.create({
        id: 'simaAnalyze',
        title: '使用史记助手分析',
        contexts: ['selection']
    });
});

// 处理右键菜单点击
chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'simaAnalyze' && info.selectionText) {
        processText(info.selectionText, 'analyze', tab.id);
    }
});

// 处理来自content script的消息
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'process') {
        processText(request.text, request.action, sender.tab.id)
            .then(response => sendResponse(response))
            .catch(error => {
                console.error('处理错误:', error);
                sendResponse({ status: 'error', message: '处理失败' });
            });
        return true;
    }
});

// 处理文本的主要函数
async function processText(text, action, tabId) {
    try {
        const apiUrl = 'http://localhost:5000/process';
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                action: action
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return {
            status: 'success',
            message: data.message
        };
    } catch (error) {
        console.error('API请求错误:', error);
        return {
            status: 'error',
            message: '处理失败，请检查服务器连接'
        };
    }
} 