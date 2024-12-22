// 获取DOM元素
const apiKeyInput = document.getElementById('apiKey');
const serverUrlInput = document.getElementById('serverUrl');
const saveButton = document.getElementById('save');
const statusDiv = document.getElementById('status');

// 加载保存的设置
chrome.storage.sync.get(['apiKey', 'serverUrl'], function(items) {
    apiKeyInput.value = items.apiKey || '';
    serverUrlInput.value = items.serverUrl || 'http://localhost:5000';
});

// 保存设置
saveButton.addEventListener('click', function() {
    const apiKey = apiKeyInput.value.trim();
    const serverUrl = serverUrlInput.value.trim();

    // 验证服务器URL
    try {
        new URL(serverUrl);
    } catch (e) {
        showStatus('请输入有效的服务器地址', 'error');
        return;
    }

    // 保存设置
    chrome.storage.sync.set({
        apiKey: apiKey,
        serverUrl: serverUrl
    }, function() {
        showStatus('设置已保存', 'success');
    });
});

// 显示状态信息
function showStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = 'status ' + type;
    statusDiv.style.display = 'block';

    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 3000);
} 