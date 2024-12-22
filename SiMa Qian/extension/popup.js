document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('input');
    const submit = document.getElementById('submit');
    const result = document.getElementById('result');

    submit.addEventListener('click', async function() {
        const text = input.value.trim();
        if (!text) {
            result.textContent = '请输入问题';
            return;
        }

        result.textContent = '处理中...';
        try {
            // TODO: 实现与后端API的通信
            const response = await fetch('http://localhost:5000/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: text })
            });

            const data = await response.json();
            result.textContent = data.message;
        } catch (error) {
            result.textContent = '处理出错，请稍后重试';
            console.error('Error:', error);
        }
    });
}); 