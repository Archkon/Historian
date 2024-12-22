from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QGroupBox, QCheckBox, QSpinBox, QDoubleSpinBox, QTabWidget, QListWidget,
    QMessageBox, QFileDialog, QScrollArea, QGridLayout, QStatusBar, QProgressBar,
    QDockWidget, QStyleFactory)
from PyQt6.QtCore import Qt, QSettings
import sys
import os
import json
from dotenv import load_dotenv
from agents.rag.rag_agent import RAGAgent
from agents.tools.tool_agent import ToolAgent
from agents.memory.memory_agent import MemoryAgent
from agents.router.router_agent import RouterAgent
from agents.reasoning.reasoning_agent import ReasoningAgent
import logging

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('Historian', 'GUI')
        self.workflows = []
        self.current_workflow = []
        
        # 设置日志记录器
        self.logger = logging.getLogger('Historian')
        self.logger.setLevel(logging.INFO)
        
        # 创建处理器
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('historian.log')
        
        # 创建格式器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self.translations = {
            "English": {
                "task_input": "Task Input",
                "agents": "Agents",
                "reasoning": "Reasoning Techniques",
                "submit": "Submit",
                "output": "Output",
                "api_settings": "API Settings",
                "model_settings": "Model Settings",
                "language_settings": "Language Settings",
                "save_settings": "Save Settings",
                "workflow": "Workflow",
                "add_step": "Add Step",
                "remove_step": "Remove Step",
                "move_up": "Move Up",
                "move_down": "Move Down",
                "save_workflow": "Save Workflow",
                "load_workflow": "Load Workflow",
                "error": "Error",
                "success": "Success",
                "settings_saved": "Settings saved",
                "workflow_saved": "Workflow saved",
                "workflow_loaded": "Workflow loaded",
                "please_enter_task": "Please enter a task",
                "processing": "Processing...",
                "no_api_key": "No API key set",
                "ready": "Ready",
                "log_viewer": "Log Viewer"
            },
            "中文": {
                "task_input": "任务输入",
                "agents": "代理选择",
                "reasoning": "推理技巧",
                "submit": "提交任务",
                "output": "输出结果",
                "api_settings": "API设置",
                "model_settings": "模型设置",
                "language_settings": "语言设置",
                "save_settings": "保存设置",
                "workflow": "工作流",
                "add_step": "添加步骤",
                "remove_step": "删除步骤",
                "move_up": "上移",
                "move_down": "下移",
                "save_workflow": "保存工作流",
                "load_workflow": "加载工作流",
                "error": "错误",
                "success": "成功",
                "settings_saved": "设置已保存",
                "workflow_saved": "工作流已保存",
                "workflow_loaded": "工作流已加载",
                "please_enter_task": "请输入任务",
                "processing": "正在处理...",
                "no_api_key": "未设置API密钥",
                "ready": "就绪",
                "log_viewer": "日志查看器"
            }
        }
        self.current_language = "English"
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Historian")
        self.setMinimumSize(1600, 1000)
        
        # Load environment variables
        load_dotenv()
        
        # Create central widget with scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create scroll areas for each panel
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        middle_scroll = QScrollArea()
        middle_scroll.setWidgetResizable(True)
        
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Create panels
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        left_panel.setMinimumWidth(400)
        
        middle_panel = QWidget()
        middle_layout = QVBoxLayout()
        middle_panel.setLayout(middle_layout)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)
        right_panel.setMinimumWidth(350)
        
        # Set panels to scroll areas
        left_scroll.setWidget(left_panel)
        middle_scroll.setWidget(middle_panel)
        right_scroll.setWidget(right_panel)
        
        # Add scroll areas to main layout
        main_layout.addWidget(left_scroll, 1)
        main_layout.addWidget(middle_scroll, 2)
        main_layout.addWidget(right_scroll, 1)
        
        # API Settings
        self.api_group = QGroupBox(self.tr("api_settings"))
        api_layout = QVBoxLayout()
        self.api_group.setLayout(api_layout)
        
        # Base URL with tooltip
        base_url_layout = QHBoxLayout()
        base_url_label = QLabel("Base URL:")
        self.base_url_input = QLineEdit()
        self.base_url_input.setText("https://api.openai.com/v1")
        self.base_url_input.setPlaceholderText("Enter API base URL")
        self.base_url_input.setToolTip("The base URL for the API service")
        base_url_layout.addWidget(base_url_label, 1)
        base_url_layout.addWidget(self.base_url_input, 2)
        api_layout.addLayout(base_url_layout)
        
        # API Key with tooltip
        api_key_layout = QHBoxLayout()
        api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Enter your API key")
        self.api_key_input.setToolTip("Your API key for authentication")
        api_key_layout.addWidget(api_key_label, 1)
        api_key_layout.addWidget(self.api_key_input, 2)
        api_layout.addLayout(api_key_layout)
        
        # Organization ID with tooltip
        org_id_layout = QHBoxLayout()
        org_id_label = QLabel("Organization ID:")
        self.org_id_input = QLineEdit()
        self.org_id_input.setPlaceholderText("Optional: Enter organization ID")
        self.org_id_input.setToolTip("Optional: Your organization ID")
        org_id_layout.addWidget(org_id_label, 1)
        org_id_layout.addWidget(self.org_id_input, 2)
        api_layout.addLayout(org_id_layout)
        
        # Model Settings
        self.model_group = QGroupBox(self.tr("model_settings"))
        model_layout = QVBoxLayout()
        self.model_group.setLayout(model_layout)
        
        # Model selection with tooltip
        model_name_layout = QHBoxLayout()
        model_name_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "claude-2"])
        self.model_combo.setEditable(True)
        self.model_combo.setToolTip("Select or enter the model name")
        model_name_layout.addWidget(model_name_label, 1)
        model_name_layout.addWidget(self.model_combo, 2)
        model_layout.addLayout(model_name_layout)
        
        # Model parameters
        params_group = QGroupBox("Model Parameters")
        params_layout = QGridLayout()
        params_group.setLayout(params_layout)
        
        # Add parameters to grid layout
        row = 0
        # Temperature
        params_layout.addWidget(QLabel("Temperature:"), row, 0)
        self.temp_spin = QDoubleSpinBox()
        self.temp_spin.setRange(0.0, 2.0)
        self.temp_spin.setSingleStep(0.1)
        self.temp_spin.setValue(0.7)
        self.temp_spin.setToolTip("Controls randomness (0.0 = deterministic, 2.0 = very random)")
        params_layout.addWidget(self.temp_spin, row, 1)
        
        row += 1
        # Top P
        params_layout.addWidget(QLabel("Top P:"), row, 0)
        self.top_p_spin = QDoubleSpinBox()
        self.top_p_spin.setRange(0.0, 1.0)
        self.top_p_spin.setSingleStep(0.1)
        self.top_p_spin.setValue(1.0)
        self.top_p_spin.setToolTip("Controls diversity via nucleus sampling")
        params_layout.addWidget(self.top_p_spin, row, 1)
        
        row += 1
        # Top K
        params_layout.addWidget(QLabel("Top K:"), row, 0)
        self.top_k_spin = QSpinBox()
        self.top_k_spin.setRange(0, 100)
        self.top_k_spin.setValue(50)
        self.top_k_spin.setToolTip("Limits the number of tokens considered for each step")
        params_layout.addWidget(self.top_k_spin, row, 1)
        
        row += 1
        # Max Tokens
        params_layout.addWidget(QLabel("Max Tokens:"), row, 0)
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(1, 4096)
        self.max_tokens_spin.setValue(2000)
        self.max_tokens_spin.setToolTip("Maximum number of tokens to generate")
        params_layout.addWidget(self.max_tokens_spin, row, 1)
        
        row += 1
        # Presence Penalty
        params_layout.addWidget(QLabel("Presence Penalty:"), row, 0)
        self.presence_penalty_spin = QDoubleSpinBox()
        self.presence_penalty_spin.setRange(-2.0, 2.0)
        self.presence_penalty_spin.setSingleStep(0.1)
        self.presence_penalty_spin.setValue(0.0)
        self.presence_penalty_spin.setToolTip("Penalizes new tokens based on their presence in the text")
        params_layout.addWidget(self.presence_penalty_spin, row, 1)
        
        row += 1
        # Frequency Penalty
        params_layout.addWidget(QLabel("Frequency Penalty:"), row, 0)
        self.frequency_penalty_spin = QDoubleSpinBox()
        self.frequency_penalty_spin.setRange(-2.0, 2.0)
        self.frequency_penalty_spin.setSingleStep(0.1)
        self.frequency_penalty_spin.setValue(0.0)
        self.frequency_penalty_spin.setToolTip("Penalizes new tokens based on their frequency in the text")
        params_layout.addWidget(self.frequency_penalty_spin, row, 1)
        
        model_layout.addWidget(params_group)
        
        # Language settings
        language_group = QGroupBox("Language Settings")
        language_layout = QHBoxLayout()
        language_group.setLayout(language_layout)
        
        language_label = QLabel("Interface Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "中文"])
        self.language_combo.setCurrentText(self.current_language)
        self.language_combo.currentTextChanged.connect(self.change_language)
        self.language_combo.setToolTip("Select interface language")
        language_layout.addWidget(language_label, 1)
        language_layout.addWidget(self.language_combo, 2)
        
        # Add groups to left panel
        left_layout.addWidget(self.api_group)
        left_layout.addWidget(self.model_group)
        left_layout.addWidget(language_group)
        
        # Agent Selection Area
        agent_group = QGroupBox("Agent Selection")
        agent_layout = QVBoxLayout()
        agent_group.setLayout(agent_layout)
        
        # RAG Agent and components
        rag_group = QGroupBox("RAG Agent")
        rag_layout = QVBoxLayout()
        self.rag_check = QCheckBox("Enable RAG")
        self.rag_check.setToolTip("Enable Retrieval-Augmented Generation")
        self.embedding_check = QCheckBox("Embedding Agent")
        self.embedding_check.setToolTip("Handle text embeddings")
        self.database_check = QCheckBox("Database Agent")
        self.database_check.setToolTip("Manage vector database")
        self.retrieval_check = QCheckBox("Retrieval Agent")
        self.retrieval_check.setToolTip("Handle document retrieval")
        self.rerank_check = QCheckBox("Rerank Agent")
        self.rerank_check.setToolTip("Rerank retrieved documents")
        
        rag_layout.addWidget(self.rag_check)
        rag_layout.addWidget(self.embedding_check)
        rag_layout.addWidget(self.database_check)
        rag_layout.addWidget(self.retrieval_check)
        rag_layout.addWidget(self.rerank_check)
        rag_group.setLayout(rag_layout)
        agent_layout.addWidget(rag_group)
        
        # Tool Agent and components
        tool_group = QGroupBox("Tool Agent")
        tool_layout = QVBoxLayout()
        self.tool_check = QCheckBox("Enable Tool")
        self.tool_check.setToolTip("Enable Tool Agent")
        self.code_check = QCheckBox("Code Tool")
        self.code_check.setToolTip("Handle code-related tasks")
        self.shell_check = QCheckBox("Shell Tool")
        self.shell_check.setToolTip("Execute shell commands")
        self.web_check = QCheckBox("Web Tool")
        self.web_check.setToolTip("Handle web interactions")
        self.file_check = QCheckBox("File Tool")
        self.file_check.setToolTip("Handle file operations")
        
        tool_layout.addWidget(self.tool_check)
        tool_layout.addWidget(self.code_check)
        tool_layout.addWidget(self.shell_check)
        tool_layout.addWidget(self.web_check)
        tool_layout.addWidget(self.file_check)
        tool_group.setLayout(tool_layout)
        agent_layout.addWidget(tool_group)
        
        # Memory Agent
        memory_group = QGroupBox("Memory Agent")
        memory_layout = QVBoxLayout()
        self.memory_check = QCheckBox("Enable Memory")
        self.memory_check.setToolTip("Enable Memory Agent")
        self.conversation_memory_check = QCheckBox("Conversation Memory")
        self.conversation_memory_check.setToolTip("Store conversation history")
        self.summary_memory_check = QCheckBox("Summary Memory")
        self.summary_memory_check.setToolTip("Generate and store summaries")
        self.vector_memory_check = QCheckBox("Vector Memory")
        self.vector_memory_check.setToolTip("Store vector representations")
        
        memory_layout.addWidget(self.memory_check)
        memory_layout.addWidget(self.conversation_memory_check)
        memory_layout.addWidget(self.summary_memory_check)
        memory_layout.addWidget(self.vector_memory_check)
        memory_group.setLayout(memory_layout)
        agent_layout.addWidget(memory_group)
        
        # Router Agent and components
        router_group = QGroupBox("Router Agent")
        router_layout = QVBoxLayout()
        self.router_check = QCheckBox("Enable Router")
        self.router_check.setToolTip("Enable Router Agent")
        self.output_agent_check = QCheckBox("Output Agent")
        self.output_agent_check.setToolTip("Handle output formatting")
        self.evaluation_agent_check = QCheckBox("Evaluation Agent")
        self.evaluation_agent_check.setToolTip("Evaluate responses")
        self.prompt_agent_check = QCheckBox("Prompt Agent")
        self.prompt_agent_check.setToolTip("Handle prompt engineering")
        
        router_layout.addWidget(self.router_check)
        router_layout.addWidget(self.output_agent_check)
        router_layout.addWidget(self.evaluation_agent_check)
        router_layout.addWidget(self.prompt_agent_check)
        router_group.setLayout(router_layout)
        agent_layout.addWidget(router_group)
        
        # Reasoning Agent and techniques
        reasoning_group = QGroupBox("Reasoning Agent")
        reasoning_layout = QVBoxLayout()
        self.reasoning_check = QCheckBox("Enable Reasoning")
        self.reasoning_check.setToolTip("Enable Reasoning Agent")
        
        # Reasoning techniques
        techniques_group = QGroupBox("Reasoning Techniques")
        techniques_layout = QVBoxLayout()
        
        self.zero_shot_check = QCheckBox("Zero-shot")
        self.zero_shot_check.setToolTip("Reason without examples")
        self.few_shot_check = QCheckBox("Few-shot")
        self.few_shot_check.setToolTip("Reason with few examples")
        self.one_shot_check = QCheckBox("One-shot")
        self.one_shot_check.setToolTip("Reason with one example")
        self.cot_check = QCheckBox("Chain of Thought")
        self.cot_check.setToolTip("Step-by-step reasoning")
        self.least_to_most_check = QCheckBox("Least to Most")
        self.least_to_most_check.setToolTip("Break down complex problems")
        self.self_consistency_check = QCheckBox("Self-consistency")
        self.self_consistency_check.setToolTip("Multiple reasoning paths")
        self.react_check = QCheckBox("ReAct")
        self.react_check.setToolTip("Reasoning and Acting")
        self.reflection_check = QCheckBox("Reflection")
        self.reflection_check.setToolTip("Self-reflection on reasoning")
        self.tot_check = QCheckBox("Tree of Thoughts")
        self.tot_check.setToolTip("Explore multiple reasoning branches")
        
        techniques_layout.addWidget(self.zero_shot_check)
        techniques_layout.addWidget(self.few_shot_check)
        techniques_layout.addWidget(self.one_shot_check)
        techniques_layout.addWidget(self.cot_check)
        techniques_layout.addWidget(self.least_to_most_check)
        techniques_layout.addWidget(self.self_consistency_check)
        techniques_layout.addWidget(self.react_check)
        techniques_layout.addWidget(self.reflection_check)
        techniques_layout.addWidget(self.tot_check)
        
        techniques_group.setLayout(techniques_layout)
        reasoning_layout.addWidget(self.reasoning_check)
        reasoning_layout.addWidget(techniques_group)
        reasoning_group.setLayout(reasoning_layout)
        
        agent_layout.addWidget(reasoning_group)
        
        # Save Settings button
        save_settings_btn = QPushButton("Save Settings")
        save_settings_btn.clicked.connect(self.save_settings)
        save_settings_btn.setToolTip("Save all settings")
        agent_layout.addWidget(save_settings_btn)
        
        left_layout.addWidget(agent_group)
        
        # Task Area (Middle Panel)
        self.task_group = QGroupBox(self.tr("task_input"))
        task_layout = QVBoxLayout()
        self.task_group.setLayout(task_layout)
        
        self.task_input = QTextEdit()
        self.task_input.setMinimumHeight(200)
        self.task_input.setPlaceholderText("Enter your task here...")
        task_layout.addWidget(self.task_input)
        
        self.submit_btn = QPushButton(self.tr("submit"))
        self.submit_btn.clicked.connect(self.submit_task)
        self.submit_btn.setToolTip("Submit task for processing")
        task_layout.addWidget(self.submit_btn)
        
        middle_layout.addWidget(self.task_group)
        
        # Output Area
        self.output_group = QGroupBox(self.tr("output"))
        output_layout = QVBoxLayout()
        self.output_group.setLayout(output_layout)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(400)
        output_layout.addWidget(self.output_text)
        
        middle_layout.addWidget(self.output_group)
        
        # Workflow Area (Right Panel)
        self.workflow_group = QGroupBox(self.tr("workflow"))
        workflow_layout = QVBoxLayout()
        self.workflow_group.setLayout(workflow_layout)
        
        self.workflow_list = QListWidget()
        self.workflow_list.setMinimumHeight(300)
        workflow_layout.addWidget(self.workflow_list)
        
        # Workflow buttons
        button_layout = QGridLayout()
        
        self.add_step_btn = QPushButton(self.tr("add_step"))
        self.add_step_btn.clicked.connect(self.add_workflow_step)
        self.add_step_btn.setToolTip("Add current configuration as workflow step")
        
        self.remove_step_btn = QPushButton(self.tr("remove_step"))
        self.remove_step_btn.clicked.connect(self.remove_workflow_step)
        self.remove_step_btn.setToolTip("Remove selected workflow step")
        
        self.move_up_btn = QPushButton(self.tr("move_up"))
        self.move_up_btn.clicked.connect(self.move_step_up)
        self.move_up_btn.setToolTip("Move selected step up")
        
        self.move_down_btn = QPushButton(self.tr("move_down"))
        self.move_down_btn.clicked.connect(self.move_step_down)
        self.move_down_btn.setToolTip("Move selected step down")
        
        button_layout.addWidget(self.add_step_btn, 0, 0)
        button_layout.addWidget(self.remove_step_btn, 0, 1)
        button_layout.addWidget(self.move_up_btn, 1, 0)
        button_layout.addWidget(self.move_down_btn, 1, 1)
        
        workflow_layout.addLayout(button_layout)
        
        # Save/Load Workflow buttons
        save_load_layout = QHBoxLayout()
        
        self.save_workflow_btn = QPushButton(self.tr("save_workflow"))
        self.save_workflow_btn.clicked.connect(self.save_workflow)
        self.save_workflow_btn.setToolTip("Save current workflow to file")
        
        self.load_workflow_btn = QPushButton(self.tr("load_workflow"))
        self.load_workflow_btn.clicked.connect(self.load_workflow)
        self.load_workflow_btn.setToolTip("Load workflow from file")
        
        save_load_layout.addWidget(self.save_workflow_btn)
        save_load_layout.addWidget(self.load_workflow_btn)
        
        workflow_layout.addLayout(save_load_layout)
        
        right_layout.addWidget(self.workflow_group)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.hide()
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Create theme selector
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(QStyleFactory.keys())
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_widget = QWidget()
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(self.theme_combo)
        theme_widget.setLayout(theme_layout)
        self.status_bar.addPermanentWidget(theme_widget)
        
        # Create log viewer dock widget
        self.log_dock = QDockWidget(self.tr("log_viewer"), self)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_dock.setWidget(self.log_text)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dock)
        
        # Load saved settings
        self.load_settings()
        
    def tr(self, key):
        """Translate text"""
        return self.translations[self.current_language].get(key, key)
        
    def submit_task(self):
        """Submit task"""
        task = self.task_input.toPlainText()
        if not task:
            QMessageBox.warning(self, self.tr("error"), self.tr("please_enter_task"))
            return
        
        api_key = self.api_key_input.text() or os.getenv("OPENAI_API_KEY")
        if not api_key:
            QMessageBox.warning(self, self.tr("error"), self.tr("no_api_key"))
            return
        
        # 确保API密钥被设置到环境变量中
        os.environ["OPENAI_API_KEY"] = api_key
        
        try:
            self.logger.info("Starting task processing")
            self.status_bar.showMessage("Processing task...")
            self.show_progress(True)
            self.output_text.setText(self.tr("processing"))
            QApplication.processEvents()
            
            # Get common parameters
            common_params = {
                "model_name": self.model_combo.currentText(),
                "api_key": self.api_key_input.text(),
                "api_base": self.base_url_input.text()
            }
            
            # Get model parameters
            model_params = {
                "temperature": self.temp_spin.value(),
                "top_p": self.top_p_spin.value(),
                "top_k": self.top_k_spin.value(),
                "max_tokens": self.max_tokens_spin.value(),
                "presence_penalty": self.presence_penalty_spin.value(),
                "frequency_penalty": self.frequency_penalty_spin.value()
            }
            
            # Initialize agents
            agents = []
            
            # RAG Agent and its components
            if self.rag_check.isChecked():
                rag_params = common_params.copy()
                rag_params.update({
                    "use_embedding": self.embedding_check.isChecked(),
                    "use_database": self.database_check.isChecked(),
                    "use_retrieval": self.retrieval_check.isChecked(),
                    "use_rerank": self.rerank_check.isChecked()
                })
                agents.append(RAGAgent(**rag_params))
                
            # Tool Agent and its components
            if self.tool_check.isChecked():
                tool_params = common_params.copy()
                tool_params.update(model_params)
                tool_params.update({
                    "use_code_tool": self.code_check.isChecked(),
                    "use_shell_tool": self.shell_check.isChecked(),
                    "use_web_tool": self.web_check.isChecked(),
                    "use_file_tool": self.file_check.isChecked()
                })
                agents.append(ToolAgent(**tool_params))
                
            # Memory Agent and its components
            if self.memory_check.isChecked():
                memory_params = common_params.copy()
                memory_params.update(model_params)
                memory_params.update({
                    "use_conversation_memory": self.conversation_memory_check.isChecked(),
                    "use_summary_memory": self.summary_memory_check.isChecked(),
                    "use_vector_memory": self.vector_memory_check.isChecked()
                })
                agents.append(MemoryAgent(**memory_params))
                
            # Router Agent and its components
            if self.router_check.isChecked():
                router_params = common_params.copy()
                router_params.update(model_params)
                router_params.update({
                    "use_output_agent": self.output_agent_check.isChecked(),
                    "use_evaluation_agent": self.evaluation_agent_check.isChecked(),
                    "use_prompt_agent": self.prompt_agent_check.isChecked()
                })
                router = RouterAgent(**router_params)
                if agents:
                    router.register_agents({
                        "rag": agents[0] if self.rag_check.isChecked() else None,
                        "tool": agents[1] if self.tool_check.isChecked() else None,
                        "memory": agents[2] if self.memory_check.isChecked() else None
                    })
                agents.append(router)
                
            # Reasoning Agent
            if self.reasoning_check.isChecked():
                reasoning_params = common_params.copy()
                reasoning_params.update(model_params)
                reasoning_params.update({
                    "reasoning_techniques": {
                        "zero_shot": self.zero_shot_check.isChecked(),
                        "few_shot": self.few_shot_check.isChecked(),
                        "one_shot": self.one_shot_check.isChecked(),
                        "cot": self.cot_check.isChecked(),
                        "least_to_most": self.least_to_most_check.isChecked(),
                        "self_consistency": self.self_consistency_check.isChecked(),
                        "react": self.react_check.isChecked(),
                        "reflection": self.reflection_check.isChecked(),
                        "tot": self.tot_check.isChecked()
                    }
                })
                agents.append(ReasoningAgent(**reasoning_params))
                
            if not agents:
                # If no agent is selected, use RAG agent by default
                agents.append(RAGAgent(**common_params))
                
            # Process task
            result = task
            for agent in agents:
                result = agent.process(task, result)
                
            self.output_text.setText(result)
            self.logger.info("Task processing completed")
            self.status_bar.showMessage("Task completed", 5000)  # Show for 5 seconds
            
        except Exception as e:
            self.logger.error(f"Error processing task: {str(e)}")
            QMessageBox.critical(self, self.tr("error"), str(e))
        finally:
            self.show_progress(False)
        
    def save_settings(self):
        """Save settings"""
        try:
            # Save API settings
            api_key = self.api_key_input.text()
            os.environ["OPENAI_API_KEY"] = api_key
            self.settings.setValue("api_key", api_key)
            os.environ["OPENAI_API_BASE"] = self.base_url_input.text()
            if self.org_id_input.text():
                os.environ["OPENAI_ORG_ID"] = self.org_id_input.text()
            
            # Save other settings
            self.settings.setValue("base_url", self.base_url_input.text())
            self.settings.setValue("org_id", self.org_id_input.text())
            
            # Save RAG Agent settings
            self.settings.setValue("use_embedding", self.embedding_check.isChecked())
            self.settings.setValue("use_database", self.database_check.isChecked())
            self.settings.setValue("use_retrieval", self.retrieval_check.isChecked())
            self.settings.setValue("use_rerank", self.rerank_check.isChecked())
            
            # Save Tool Agent settings
            self.settings.setValue("use_code_tool", self.code_check.isChecked())
            self.settings.setValue("use_shell_tool", self.shell_check.isChecked())
            self.settings.setValue("use_web_tool", self.web_check.isChecked())
            self.settings.setValue("use_file_tool", self.file_check.isChecked())
            
            # Save Memory Agent settings
            self.settings.setValue("use_conversation_memory", self.conversation_memory_check.isChecked())
            self.settings.setValue("use_summary_memory", self.summary_memory_check.isChecked())
            self.settings.setValue("use_vector_memory", self.vector_memory_check.isChecked())
            
            # Save Router Agent settings
            self.settings.setValue("use_output_agent", self.output_agent_check.isChecked())
            self.settings.setValue("use_evaluation_agent", self.evaluation_agent_check.isChecked())
            self.settings.setValue("use_prompt_agent", self.prompt_agent_check.isChecked())
            
            # Save model parameters
            self.settings.setValue("model", self.model_combo.currentText())
            self.settings.setValue("language", self.current_language)
            
            # Save model parameters
            self.settings.setValue("temperature", self.temp_spin.value())
            self.settings.setValue("top_p", self.top_p_spin.value())
            self.settings.setValue("top_k", self.top_k_spin.value())
            self.settings.setValue("max_tokens", self.max_tokens_spin.value())
            self.settings.setValue("presence_penalty", self.presence_penalty_spin.value())
            self.settings.setValue("frequency_penalty", self.frequency_penalty_spin.value())
            
            # Save agent selection status
            self.settings.setValue("use_rag", self.rag_check.isChecked())
            self.settings.setValue("use_tool", self.tool_check.isChecked())
            self.settings.setValue("use_memory", self.memory_check.isChecked())
            self.settings.setValue("use_router", self.router_check.isChecked())
            self.settings.setValue("use_reasoning", self.reasoning_check.isChecked())
            
            # Save reasoning technique status
            self.settings.setValue("zero_shot", self.zero_shot_check.isChecked())
            self.settings.setValue("few_shot", self.few_shot_check.isChecked())
            self.settings.setValue("one_shot", self.one_shot_check.isChecked())
            self.settings.setValue("cot", self.cot_check.isChecked())
            self.settings.setValue("least_to_most", self.least_to_most_check.isChecked())
            self.settings.setValue("self_consistency", self.self_consistency_check.isChecked())
            self.settings.setValue("react", self.react_check.isChecked())
            self.settings.setValue("reflection", self.reflection_check.isChecked())
            self.settings.setValue("tot", self.tot_check.isChecked())
            
            QMessageBox.information(self, self.tr("success"), self.tr("settings_saved"))
            
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), str(e))
        
    def load_settings(self):
        """Load settings"""
        try:
            # Load API settings
            self.base_url_input.setText(self.settings.value("base_url", "https://api.openai.com/v1"))
            saved_api_key = self.settings.value("api_key", "")
            self.api_key_input.setText(saved_api_key)
            if saved_api_key:
                os.environ["OPENAI_API_KEY"] = saved_api_key
            self.org_id_input.setText(self.settings.value("org_id", ""))
            
            # Load model parameters
            self.model_combo.setCurrentText(self.settings.value("model", "gpt-3.5-turbo"))
            self.change_language(self.settings.value("language", "English"))
            
            # Load RAG Agent settings
            self.embedding_check.setChecked(self.settings.value("use_embedding", False, type=bool))
            self.database_check.setChecked(self.settings.value("use_database", False, type=bool))
            self.retrieval_check.setChecked(self.settings.value("use_retrieval", False, type=bool))
            self.rerank_check.setChecked(self.settings.value("use_rerank", False, type=bool))
            
            # Load Tool Agent settings
            self.code_check.setChecked(self.settings.value("use_code_tool", False, type=bool))
            self.shell_check.setChecked(self.settings.value("use_shell_tool", False, type=bool))
            self.web_check.setChecked(self.settings.value("use_web_tool", False, type=bool))
            self.file_check.setChecked(self.settings.value("use_file_tool", False, type=bool))
            
            # Load Memory Agent settings
            self.conversation_memory_check.setChecked(self.settings.value("use_conversation_memory", False, type=bool))
            self.summary_memory_check.setChecked(self.settings.value("use_summary_memory", False, type=bool))
            self.vector_memory_check.setChecked(self.settings.value("use_vector_memory", False, type=bool))
            
            # Load Router Agent settings
            self.output_agent_check.setChecked(self.settings.value("use_output_agent", False, type=bool))
            self.evaluation_agent_check.setChecked(self.settings.value("use_evaluation_agent", False, type=bool))
            self.prompt_agent_check.setChecked(self.settings.value("use_prompt_agent", False, type=bool))
            
            # Load model parameters
            self.temp_spin.setValue(float(self.settings.value("temperature", 0.7)))
            self.top_p_spin.setValue(float(self.settings.value("top_p", 1.0)))
            self.top_k_spin.setValue(int(self.settings.value("top_k", 50)))
            self.max_tokens_spin.setValue(int(self.settings.value("max_tokens", 2000)))
            self.presence_penalty_spin.setValue(float(self.settings.value("presence_penalty", 0.0)))
            self.frequency_penalty_spin.setValue(float(self.settings.value("frequency_penalty", 0.0)))
            
            # Load agent selection status
            self.rag_check.setChecked(self.settings.value("use_rag", False, type=bool))
            self.tool_check.setChecked(self.settings.value("use_tool", False, type=bool))
            self.memory_check.setChecked(self.settings.value("use_memory", False, type=bool))
            self.router_check.setChecked(self.settings.value("use_router", False, type=bool))
            self.reasoning_check.setChecked(self.settings.value("use_reasoning", False, type=bool))
            
            # Load reasoning technique status
            self.zero_shot_check.setChecked(self.settings.value("zero_shot", False, type=bool))
            self.few_shot_check.setChecked(self.settings.value("few_shot", False, type=bool))
            self.one_shot_check.setChecked(self.settings.value("one_shot", False, type=bool))
            self.cot_check.setChecked(self.settings.value("cot", False, type=bool))
            self.least_to_most_check.setChecked(self.settings.value("least_to_most", False, type=bool))
            self.self_consistency_check.setChecked(self.settings.value("self_consistency", False, type=bool))
            self.react_check.setChecked(self.settings.value("react", False, type=bool))
            self.reflection_check.setChecked(self.settings.value("reflection", False, type=bool))
            self.tot_check.setChecked(self.settings.value("tot", False, type=bool))
            
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), str(e))
        
    def change_language(self, language: str):
        """切换界面语言"""
        self.current_language = language
        self.retranslate_ui()
        self.settings.setValue("language", language)
        self.logger.info(f"Changed language to {language}")

    def retranslate_ui(self):
        """更新界面文本"""
        # 更新窗口标题
        self.setWindowTitle(self.tr("Historian"))
        
        # 更新API设置组
        self.api_group.setTitle(self.tr("api_settings"))
        
        # 更新模型设置组
        self.model_group.setTitle(self.tr("model_settings"))
        
        # 更新任务输入组
        self.task_group.setTitle(self.tr("task_input"))
        self.submit_btn.setText(self.tr("submit"))
        
        # 更新输出组
        self.output_group.setTitle(self.tr("output"))
        
        # 更新工作流组
        self.workflow_group.setTitle(self.tr("workflow"))
        self.add_step_btn.setText(self.tr("add_step"))
        self.remove_step_btn.setText(self.tr("remove_step"))
        self.move_up_btn.setText(self.tr("move_up"))
        self.move_down_btn.setText(self.tr("move_down"))
        self.save_workflow_btn.setText(self.tr("save_workflow"))
        self.load_workflow_btn.setText(self.tr("load_workflow"))
        
        # 更新日志查看器标题
        self.log_dock.setWindowTitle(self.tr("log_viewer"))
        
        # 更新状态栏
        self.status_bar.showMessage(self.tr("ready"))

    def add_workflow_step(self):
        """Add workflow step"""
        # Get current agent and reasoning technique selections
        step = {
            "agents": {
                "rag": self.rag_check.isChecked(),
                "tool": self.tool_check.isChecked(),
                "memory": self.memory_check.isChecked(),
                "router": self.router_check.isChecked(),
                "reasoning": self.reasoning_check.isChecked()
            },
            "reasoning_techniques": {
                "zero_shot": self.zero_shot_check.isChecked(),
                "few_shot": self.few_shot_check.isChecked(),
                "one_shot": self.one_shot_check.isChecked(),
                "cot": self.cot_check.isChecked(),
                "least_to_most": self.least_to_most_check.isChecked(),
                "self_consistency": self.self_consistency_check.isChecked(),
                "react": self.react_check.isChecked(),
                "reflection": self.reflection_check.isChecked(),
                "tot": self.tot_check.isChecked()
            }
        }
        
        self.current_workflow.append(step)
        self.update_workflow_list()
        
    def remove_workflow_step(self):
        """Remove workflow step"""
        current_row = self.workflow_list.currentRow()
        if current_row >= 0:
            self.current_workflow.pop(current_row)
            self.update_workflow_list()
            
    def move_step_up(self):
        """Move workflow step up"""
        current_row = self.workflow_list.currentRow()
        if current_row > 0:
            self.current_workflow[current_row], self.current_workflow[current_row-1] = \
                self.current_workflow[current_row-1], self.current_workflow[current_row]
            self.update_workflow_list()
            self.workflow_list.setCurrentRow(current_row-1)
            
    def move_step_down(self):
        """Move workflow step down"""
        current_row = self.workflow_list.currentRow()
        if current_row >= 0 and current_row < len(self.current_workflow) - 1:
            self.current_workflow[current_row], self.current_workflow[current_row+1] = \
                self.current_workflow[current_row+1], self.current_workflow[current_row]
            self.update_workflow_list()
            self.workflow_list.setCurrentRow(current_row+1)
            
    def update_workflow_list(self):
        """Update workflow list"""
        self.workflow_list.clear()
        for i, step in enumerate(self.current_workflow):
            agents = [name for name, enabled in step["agents"].items() if enabled]
            techniques = [name for name, enabled in step["reasoning_techniques"].items() if enabled]
            self.workflow_list.addItem(f"Step {i+1}: {', '.join(agents)} - {', '.join(techniques)}")
            
    def save_workflow(self):
        """Save workflow"""
        try:
            filename, _ = QFileDialog.getSaveFileName(self, self.tr("save_workflow"), "", "JSON (*.json)")
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_workflow, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, self.tr("success"), self.tr("workflow_saved"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), str(e))
            
    def load_workflow(self):
        """Load workflow"""
        try:
            filename, _ = QFileDialog.getOpenFileName(self, self.tr("load_workflow"), "", "JSON (*.json)")
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.current_workflow = json.load(f)
                self.update_workflow_list()
                QMessageBox.information(self, self.tr("success"), self.tr("workflow_loaded"))
        except Exception as e:
            QMessageBox.critical(self, self.tr("error"), str(e))

    def show_progress(self, show=True):
        """显示或隐藏进度条"""
        if show:
            self.progress_bar.setRange(0, 0)  # 不确定进度模式
            self.progress_bar.show()
        else:
            self.progress_bar.hide()

    def change_theme(self, theme_name):
        """切换应用主题"""
        try:
            QApplication.setStyle(QStyleFactory.create(theme_name))
            self.settings.setValue("theme", theme_name)
            self.logger.info(f"Changed theme to {theme_name}")
            self.status_bar.showMessage(f"Theme changed to {theme_name}", 3000)
        except Exception as e:
            self.logger.error(f"Error changing theme: {str(e)}")
            QMessageBox.critical(self, self.tr("error"), str(e))

def main():
    """Main entry point"""
    print("Starting Historian GUI...")
    app = QApplication(sys.argv)
    print("Created QApplication")
    
    window = MainWindow()
    print("Created MainWindow")
    
    window.show()
    print("Showing window")
    
    print("Starting event loop")
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 