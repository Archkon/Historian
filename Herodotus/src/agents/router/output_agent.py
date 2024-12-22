from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class OutputAgent(BaseAgent):
    """输出代理"""
    
    ROLE = """你是一个专门负责优化输出的AI助手。

你的主要职责是：
1. 改进输出的格式和结构
2. 确保输出的清晰度和可读性
3. 添加必要的上下文信息
4. 根据需要生成不同格式的输出

请确保输出既专业又易于理解。"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name, streaming=False)
        
    def format_output(self, content: str, format_type: str = "text") -> str:
        """格式化输出"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请将以下内容转换为{format_type}格式，确保结构清晰、易于理解。"""),
            HumanMessage(content=content)
        ]
        
        return self.chat(messages)
        
    def add_context(self, content: str, context: str) -> str:
        """添加上下文信息"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请在保持原始内容的基础上，添加以下上下文信息，使输出更加完整和有意义。"""),
            HumanMessage(content=f"""原始内容：
{content}

上下文信息：
{context}""")
        ]
        
        return self.chat(messages)
        
    def summarize(self, content: str, max_length: int = 200) -> str:
        """生成摘要"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请生成一个简洁的摘要，长度不超过{max_length}个字符。
保留最重要的信息，确保摘要完整且有意义。"""),
            HumanMessage(content=content)
        ]
        
        return self.chat(messages) 