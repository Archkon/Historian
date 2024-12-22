from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import json

class MemoryAgent(BaseAgent):
    """基于语言模型的记忆代理"""
    
    ROLE = """你是一个专门管理对话记忆的AI助手。
    
    你的主要职责是：
    1. 记录对话历史
    2. 提取关键信息
    3. 总结对话内容
    4. 管理记忆检索
    请确保记忆的准确性和相关性。"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name, streaming=False)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
    def add_memory(self, human_input: str, ai_output: str) -> None:
        """添加新的对话记忆"""
        self.memory.save_context(
            {"input": human_input},
            {"output": ai_output}
        )
        
    def get_memory(self) -> List[Dict]:
        """获取对话历史"""
        return self.memory.load_memory_variables({})["chat_history"]
        
    def clear_memory(self) -> None:
        """清除所有记忆"""
        self.memory.clear()
        
    def summarize_memory(self) -> str:
        """总结对话历史"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            请总结以下对话历史：..."""),
            HumanMessage(content=str(self.get_memory()))
        ]
        response = self.chat(messages)
        return response
        
    def extract_key_points(self) -> List[str]:
        """提取关键信息"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            请从以下对话历史中提取关键信息点：..."""),
            HumanMessage(content=str(self.get_memory()))
        ]
        response = self.chat(messages)
        return json.loads(response)
        
    def search_memory(self, query: str) -> List[Dict]:
        """搜索相关记忆"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            请在对话历史中搜索与以下查询相关的内容：..."""),
            HumanMessage(content=f"""查询：{query} 历史：{str(self.get_memory())}""")
        ]
        response = self.chat(messages)
        return json.loads(response)
        
    def evaluate_memory_quality(self) -> Dict:
        """评估记忆质量"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            请评估当前记忆的质量：..."""),
            HumanMessage(content=str(self.get_memory()))
        ]
        response = self.chat(messages)
        return json.loads(response)
        
    def optimize_memory(self) -> None:
        """优化记忆内容"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            请优化以下对话历史：..."""),
            HumanMessage(content=str(self.get_memory()))
        ]
        response = self.chat(messages)
        optimized = json.loads(response)
        self.clear_memory()
        for item in optimized:
            self.add_memory(item["input"], item["output"]) 