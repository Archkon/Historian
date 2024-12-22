document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const settingsForm = document.getElementById('settingsForm');
    const taskInput = document.getElementById('taskInput');
    const submitTask = document.getElementById('submitTask');
    const output = document.getElementById('output');
    const logViewer = document.getElementById('logViewer');
    const statusMessage = document.getElementById('statusMessage');
    const progressBar = document.getElementById('progressBar');
    const languageSelect = document.getElementById('languageSelect');
    const themeSelect = document.getElementById('themeSelect');
    const modelSelect = document.getElementById('modelSelect');
    const customModelSettings = document.getElementById('customModelSettings');
    const workflowSteps = document.getElementById('workflowSteps');
    const addWorkflowStep = document.getElementById('addWorkflowStep');
    const moveStepUp = document.getElementById('moveStepUp');
    const moveStepDown = document.getElementById('moveStepDown');
    const deleteStep = document.getElementById('deleteStep');
    const saveWorkflow = document.getElementById('saveWorkflow');
    const loadWorkflow = document.getElementById('loadWorkflow');
    const workflowList = document.getElementById('workflowList');
    
    // 获取所有range输入元素和对应的值显示元素
    const rangeInputs = {
        temperature: document.querySelector('input[name="temperature"]'),
        top_p: document.querySelector('input[name="top_p"]'),
        top_k: document.querySelector('input[name="top_k"]'),
        max_tokens: document.querySelector('input[name="max_tokens"]'),
        presence_penalty: document.querySelector('input[name="presence_penalty"]'),
        frequency_penalty: document.querySelector('input[name="frequency_penalty"]')
    };
    
    const rangeValues = {
        temperature: document.getElementById('temperatureValue'),
        top_p: document.getElementById('topPValue'),
        top_k: document.getElementById('topKValue'),
        max_tokens: document.getElementById('maxTokensValue'),
        presence_penalty: document.getElementById('presencePenaltyValue'),
        frequency_penalty: document.getElementById('frequencyPenaltyValue')
    };
    
    // 为所有range输入添加事件监听器
    Object.entries(rangeInputs).forEach(([key, input]) => {
        input.addEventListener('input', function() {
            rangeValues[key].textContent = this.value;
        });
    });

    // 主代理复选框和子组件复选框的关系
    const agentRelations = {
        useRag: ['useEmbedding', 'useDatabase', 'useRetrieval', 'useRerank'],
        useTool: ['useCodeTool', 'useShellTool', 'useWebTool', 'useFileTool'],
        useMemory: ['useConversationMemory', 'useSummaryMemory', 'useVectorMemory'],
        useRouter: ['useOutputAgent', 'useEvaluationAgent', 'usePromptAgent'],
        useReasoning: ['zeroShot', 'fewShot', 'oneShot', 'cot', 'leastToMost', 'selfConsistency', 'react', 'reflection', 'tot']
    };
    
    // 为主代理复选框添加事件监听器
    Object.entries(agentRelations).forEach(([mainAgent, subAgents]) => {
        const mainCheckbox = document.getElementById(mainAgent);
        mainCheckbox.addEventListener('change', function() {
            subAgents.forEach(subAgent => {
                const subCheckbox = document.getElementById(subAgent);
                subCheckbox.disabled = !this.checked;
                if (!this.checked) {
                    subCheckbox.checked = false;
                }
            });
        });
    });

    // 语言配置
    const translations = {
        zh: {
            taskPlaceholder: '请输入您的任务...',
            submitTask: '提交任务',
            settings: '设置',
            modelSettings: '模型设置',
            apiSettings: 'API设置',
            ragAgent: 'RAG代理',
            toolAgent: '工具代理',
            memoryAgent: '记忆代理',
            routerAgent: '路由代理',
            reasoningAgent: '推理代理',
            workflow: '工作流',
            addStep: '添加步骤',
            save: '保存',
            load: '加载',
            ready: '就绪',
            processing: '处理中...',
            success: '成功',
            error: '错误'
        },
        en: {
            taskPlaceholder: 'Enter your task...',
            submitTask: 'Submit Task',
            settings: 'Settings',
            modelSettings: 'Model Settings',
            apiSettings: 'API Settings',
            ragAgent: 'RAG Agent',
            toolAgent: 'Tool Agent',
            memoryAgent: 'Memory Agent',
            routerAgent: 'Router Agent',
            reasoningAgent: 'Reasoning Agent',
            workflow: 'Workflow',
            addStep: 'Add Step',
            save: 'Save',
            load: 'Load',
            ready: 'Ready',
            processing: 'Processing...',
            success: 'Success',
            error: 'Error'
        }
    };

    // 切换语言
    function changeLanguage(language) {
        const texts = translations[language];
        if (!texts) return;

        // 更新页面文本
        taskInput.placeholder = texts.taskPlaceholder;
        submitTask.textContent = texts.submitTask;
        document.querySelector('.card-header h5').textContent = texts.settings;
        
        // 更新按钮文本
        addWorkflowStep.innerHTML = `<i class="bi bi-plus"></i> ${texts.addStep}`;
        saveWorkflow.innerHTML = `<i class="bi bi-save"></i> ${texts.save}`;
        loadWorkflow.innerHTML = `<i class="bi bi-folder-open"></i> ${texts.load}`;

        // 更新状态文本
        if (statusMessage.textContent === '就绪' || statusMessage.textContent === 'Ready') {
            statusMessage.textContent = texts.ready;
        }

        // 保存语言设置
        localStorage.setItem('language', language);
        addLog(`切换语言到: ${language}`);
    }

    // 主题切换
    themeSelect.addEventListener('change', function() {
        changeTheme(this.value);
    });

    // 提交任务
    submitTask.addEventListener('click', async function() {
        const task = taskInput.value.trim();
        if (!task) {
            showMessage('请输入任务内容', 'error');
            return;
        }

        // 收集设置
        const formData = new FormData(settingsForm);
        const settings = {};
        for (let [key, value] of formData.entries()) {
            if (key === 'temperature' || key === 'top_p' || key === 'top_k' || 
                key === 'max_tokens' || key === 'presence_penalty' || key === 'frequency_penalty') {
                settings[key] = parseFloat(value);
            } else if (value === 'on') {
                settings[key] = true;
            } else {
                settings[key] = value;
            }
        }

        // 显示加载状态
        showProgress(true);
        output.textContent = '处理中...';
        submitTask.disabled = true;
        updateStatus('正在处理任务...');

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task: task,
                    settings: settings
                })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                output.innerHTML = marked.parse(data.result);
                showMessage('处理完成', 'success');
                addLog('任务处理完成');
            } else {
                showMessage(data.message || '处理失败', 'error');
                addLog(`处理失败: ${data.message}`);
            }
        } catch (error) {
            showMessage('请求失败: ' + error.message, 'error');
            addLog(`请求失败: ${error.message}`);
        } finally {
            showProgress(false);
            submitTask.disabled = false;
            updateStatus('就绪');
        }
    });

    // 保存工作流
    saveWorkflow.addEventListener('click', async function() {
        const name = prompt('请输入工作流名称:');
        if (!name) return;

        try {
            const response = await fetch('/api/workflow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    steps: currentSteps
                })
            });

            const data = await response.json();
            if (data.status === 'success') {
                showMessage('工作流保存成功', 'success');
                addLog('工作流保存成功');
                loadWorkflows();
            } else {
                showMessage(data.message || '保存失败', 'error');
                addLog(`保存失败: ${data.message}`);
            }
        } catch (error) {
            showMessage('保存失败: ' + error.message, 'error');
            addLog(`保存失败: ${error.message}`);
        }
    });

    // 加载工作流
    loadWorkflow.addEventListener('click', async function() {
        try {
            const response = await fetch('/api/workflow');
            const data = await response.json();
            
            // 创建工作流选择对话框
            const dialog = document.createElement('div');
            dialog.className = 'modal fade';
            dialog.innerHTML = `
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">选择工作流</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="list-group">
                                ${data.workflows.map((workflow, index) => `
                                    <button class="list-group-item list-group-item-action workflow-item" data-index="${index}">
                                        ${workflow.name}
                                        <span class="badge bg-secondary float-end">${workflow.steps.length} 步骤</span>
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(dialog);
            const modal = new bootstrap.Modal(dialog);
            
            // 添加点击事件
            dialog.querySelectorAll('.workflow-item').forEach(item => {
                item.addEventListener('click', () => {
                    const index = parseInt(item.dataset.index);
                    currentSteps = data.workflows[index].steps;
                    selectedStepIndex = -1;
                    renderWorkflowSteps();
                    modal.hide();
                    showMessage('工作流加载成功', 'success');
                    addLog('工作流加载成功');
                });
            });
            
            modal.show();
            
            // 清理对话框
            dialog.addEventListener('hidden.bs.modal', () => {
                document.body.removeChild(dialog);
            });
        } catch (error) {
            showMessage('加载失败: ' + error.message, 'error');
            addLog(`加载失败: ${error.message}`);
        }
    });

    // 加载工作流列表
    async function loadWorkflows() {
        try {
            const response = await fetch('/api/workflow');
            const data = await response.json();
            
            workflowList.innerHTML = '';
            data.workflows.forEach((workflow, index) => {
                const item = document.createElement('a');
                item.href = '#';
                item.className = 'list-group-item list-group-item-action workflow-item';
                item.textContent = workflow.name;
                
                item.addEventListener('click', function(e) {
                    e.preventDefault();
                    applyWorkflow(workflow);
                });

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm float-end';
                deleteBtn.innerHTML = '<i class="bi bi-trash"></i>';
                deleteBtn.addEventListener('click', async function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    if (confirm('确定要删除这个工作流吗？')) {
                        await deleteWorkflow(index);
                    }
                });

                item.appendChild(deleteBtn);
                workflowList.appendChild(item);
            });
        } catch (error) {
            showMessage('加载工作流失败: ' + error.message, 'error');
        }
    }

    // 应用工作流设置
    function applyWorkflow(workflow) {
        if (!workflow.steps || !workflow.steps[0]) return;
        
        const step = workflow.steps[0];
        
        // 重置所有设置
        settingsForm.reset();
        
        // 应用代理设置
        for (let [agent, enabled] of Object.entries(step.agents)) {
            const checkbox = document.querySelector(`input[name="use_${agent}"]`);
            if (checkbox) checkbox.checked = enabled;
        }
        
        // 应用推理技巧设置
        for (let [technique, enabled] of Object.entries(step.reasoning_techniques)) {
            const checkbox = document.querySelector(`input[name="${technique}"]`);
            if (checkbox) checkbox.checked = enabled;
        }
        
        // 更新UI
        useReasoningCheck.dispatchEvent(new Event('change'));
        showMessage('工作流设置已应用', 'success');
    }

    // 删除工作流
    async function deleteWorkflow(index) {
        try {
            const response = await fetch(`/api/workflow/${index}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                showMessage('工作流删除成功', 'success');
                loadWorkflows();
            } else {
                showMessage(data.message || '删除失败', 'error');
            }
        } catch (error) {
            showMessage('删除失败: ' + error.message, 'error');
        }
    }

    // 显示消息
    function showMessage(message, type = 'success') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        messageDiv.textContent = message;
        
        output.parentNode.insertBefore(messageDiv, output.nextSibling);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    // 添加日志
    function addLog(message) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = `[${timestamp}] ${message}`;
        logViewer.appendChild(logEntry);
        logViewer.scrollTop = logViewer.scrollHeight;
    }

    // 更新状态栏
    function updateStatus(message) {
        statusMessage.textContent = message;
    }

    // 显示/隐藏进度条
    function showProgress(show) {
        progressBar.style.display = show ? 'block' : 'none';
        if (show) {
            output.classList.add('loading');
        } else {
            output.classList.remove('loading');
        }
    }

    // 切换主题
    function changeTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        addLog(`切换主题到: ${theme}`);
    }

    // 当前工作流步骤
    let currentSteps = [];
    let selectedStepIndex = -1;

    // 模型选择处理
    modelSelect.addEventListener('change', function() {
        customModelSettings.style.display = this.value === 'custom' ? 'block' : 'none';
    });

    // 工作流步骤管理
    addWorkflowStep.addEventListener('click', function() {
        const step = createWorkflowStep();
        currentSteps.push(step);
        renderWorkflowSteps();
        addLog('添加新工作流步骤');
    });

    moveStepUp.addEventListener('click', function() {
        if (selectedStepIndex > 0) {
            const temp = currentSteps[selectedStepIndex];
            currentSteps[selectedStepIndex] = currentSteps[selectedStepIndex - 1];
            currentSteps[selectedStepIndex - 1] = temp;
            selectedStepIndex--;
            renderWorkflowSteps();
            addLog('上移工作流步骤');
        }
    });

    moveStepDown.addEventListener('click', function() {
        if (selectedStepIndex < currentSteps.length - 1 && selectedStepIndex >= 0) {
            const temp = currentSteps[selectedStepIndex];
            currentSteps[selectedStepIndex] = currentSteps[selectedStepIndex + 1];
            currentSteps[selectedStepIndex + 1] = temp;
            selectedStepIndex++;
            renderWorkflowSteps();
            addLog('下移工作流步骤');
        }
    });

    deleteStep.addEventListener('click', function() {
        if (selectedStepIndex >= 0) {
            currentSteps.splice(selectedStepIndex, 1);
            selectedStepIndex = -1;
            renderWorkflowSteps();
            addLog('删除工作流步骤');
        }
    });

    // 创建工作流步骤
    function createWorkflowStep() {
        const formData = new FormData(settingsForm);
        const step = {
            model: formData.get('model'),
            custom_model: formData.get('model') === 'custom' ? {
                name: formData.get('custom_model_name')
            } : null,
            parameters: {
                temperature: parseFloat(formData.get('temperature')),
                top_p: parseFloat(formData.get('top_p')),
                top_k: parseInt(formData.get('top_k')),
                max_tokens: parseInt(formData.get('max_tokens')),
                presence_penalty: parseFloat(formData.get('presence_penalty')),
                frequency_penalty: parseFloat(formData.get('frequency_penalty'))
            },
            agents: {
                rag: formData.get('use_rag') === 'on',
                tool: formData.get('use_tool') === 'on',
                memory: formData.get('use_memory') === 'on',
                router: formData.get('use_router') === 'on',
                reasoning: formData.get('use_reasoning') === 'on'
            },
            agent_components: {
                embedding: formData.get('use_embedding') === 'on',
                database: formData.get('use_database') === 'on',
                retrieval: formData.get('use_retrieval') === 'on',
                rerank: formData.get('use_rerank') === 'on',
                code_tool: formData.get('use_code_tool') === 'on',
                shell_tool: formData.get('use_shell_tool') === 'on',
                web_tool: formData.get('use_web_tool') === 'on',
                file_tool: formData.get('use_file_tool') === 'on',
                conversation_memory: formData.get('use_conversation_memory') === 'on',
                summary_memory: formData.get('use_summary_memory') === 'on',
                vector_memory: formData.get('use_vector_memory') === 'on',
                output_agent: formData.get('use_output_agent') === 'on',
                evaluation_agent: formData.get('use_evaluation_agent') === 'on',
                prompt_agent: formData.get('use_prompt_agent') === 'on'
            },
            reasoning_techniques: {
                zero_shot: formData.get('zero_shot') === 'on',
                few_shot: formData.get('few_shot') === 'on',
                one_shot: formData.get('one_shot') === 'on',
                cot: formData.get('cot') === 'on',
                least_to_most: formData.get('least_to_most') === 'on',
                self_consistency: formData.get('self_consistency') === 'on',
                react: formData.get('react') === 'on',
                reflection: formData.get('reflection') === 'on',
                tot: formData.get('tot') === 'on'
            }
        };
        return step;
    }

    // 渲染工作流步骤
    function renderWorkflowSteps() {
        workflowSteps.innerHTML = '';
        currentSteps.forEach((step, index) => {
            const stepElement = document.createElement('div');
            stepElement.className = `workflow-step p-2 mb-2 border rounded ${index === selectedStepIndex ? 'active' : ''}`;
            
            // 创建步骤标题
            const title = document.createElement('div');
            title.className = 'd-flex justify-content-between align-items-center';
            title.innerHTML = `
                <span>步骤 ${index + 1}: ${step.model}${step.custom_model ? ` (${step.custom_model.name})` : ''}</span>
                <span class="badge bg-primary">${Object.entries(step.agents).filter(([_, v]) => v).length} 个代理</span>
            `;
            
            // 创建步骤详情
            const details = document.createElement('div');
            details.className = 'mt-2';
            details.innerHTML = `
                <div class="small">
                    <div>温度: ${step.parameters.temperature}</div>
                    <div>代理: ${Object.entries(step.agents)
                        .filter(([_, v]) => v)
                        .map(([k, _]) => k)
                        .join(', ')}</div>
                    ${step.agents.reasoning ? `
                    <div>推理技巧: ${Object.entries(step.reasoning_techniques)
                        .filter(([_, v]) => v)
                        .map(([k, _]) => k)
                        .join(', ')}</div>
                    ` : ''}
                </div>
            `;
            
            stepElement.appendChild(title);
            stepElement.appendChild(details);
            
            // 添加点击事件
            stepElement.addEventListener('click', () => {
                selectedStepIndex = index;
                renderWorkflowSteps();
                applyStepSettings(step);
            });
            
            workflowSteps.appendChild(stepElement);
        });
        
        // 更新按钮状态
        moveStepUp.disabled = selectedStepIndex <= 0;
        moveStepDown.disabled = selectedStepIndex < 0 || selectedStepIndex >= currentSteps.length - 1;
        deleteStep.disabled = selectedStepIndex < 0;
    }

    // 应用步骤设置
    function applyStepSettings(step) {
        // 设置模型
        modelSelect.value = step.model;
        customModelSettings.style.display = step.model === 'custom' ? 'block' : 'none';
        if (step.model === 'custom' && step.custom_model) {
            document.querySelector('input[name="custom_model_name"]').value = step.custom_model.name;
            document.querySelector('input[name="custom_model_endpoint"]').value = step.custom_model.endpoint;
            document.querySelector('textarea[name="custom_model_config"]').value = step.custom_model.config;
        }

        // 设置参数
        Object.entries(step.parameters).forEach(([key, value]) => {
            const input = document.querySelector(`input[name="${key}"]`);
            if (input) {
                input.value = value;
                // 触发range输入的change事件以更新显示值
                if (input.type === 'range') {
                    input.dispatchEvent(new Event('input'));
                }
            }
        });

        // 设置代理
        Object.entries(step.agents).forEach(([key, value]) => {
            const checkbox = document.querySelector(`input[name="use_${key}"]`);
            if (checkbox) {
                checkbox.checked = value;
                checkbox.dispatchEvent(new Event('change'));
            }
        });

        // 设置代理组件
        Object.entries(step.agent_components).forEach(([key, value]) => {
            const checkbox = document.querySelector(`input[name="use_${key}"]`);
            if (checkbox) {
                checkbox.checked = value;
            }
        });

        // 设置推理技巧
        Object.entries(step.reasoning_techniques).forEach(([key, value]) => {
            const checkbox = document.querySelector(`input[name="${key}"]`);
            if (checkbox) {
                checkbox.checked = value;
            }
        });
    }

    // 初始化时添加工作流相关的状态
    function initialize() {
        // 加载保存的主题
        const savedTheme = localStorage.getItem('theme') || 'light';
        themeSelect.value = savedTheme;
        changeTheme(savedTheme);

        // 加载保存的语言
        const savedLanguage = localStorage.getItem('language') || 'zh';
        languageSelect.value = savedLanguage;
        changeLanguage(savedLanguage);

        // 禁用所有子代理复选框
        Object.values(agentRelations).flat().forEach(subAgent => {
            document.getElementById(subAgent).disabled = true;
        });

        // 加载工作流列表
        loadWorkflows();

        addLog('应用初始化完成');
        updateStatus(translations[savedLanguage].ready);

        // 初始化工作流步骤列表
        renderWorkflowSteps();
    }

    // 运行初始化
    initialize();
}); 