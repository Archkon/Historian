from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class RewriteAgent(BaseAgent):
    """重写代理"""
    
    ROLE = """你是一个专门进行文本重写和转换的AI助手。

你的主要职责是：
1. 将文本块转换为问答对
2. 使用Hypothetical Document Embeddings (HyDE)技术生成假设文档
3. 改写查询以提高检索效果
4. 生成多样化的问题形式

请确保重写后的内容保持原意的同时，提高检索的效果。"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化重写代理
        
        Args:
            model_name: 模型名称
            api_key: OpenAI API密钥
            api_base: OpenAI API基础URL
            streaming: 是否启用流式输出
        """
        super().__init__(model_name=model_name, 
                        api_key=api_key, 
                        api_base=api_base,
                        streaming=streaming)
        
    def text_to_qa(self, text: str) -> List[Dict[str, str]]:
        """将文本转换为问答对"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请将以下文本转换为3-5个问答对。每个问答对应该涵盖文本的重要信息。"""),
            HumanMessage(content=text)
        ]
        
        response = self.chat(messages)
        # 处理响应，将其转换为结构化的问答对
        qa_pairs = []
        current_pair = {}
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('Q:'):
                if current_pair:
                    qa_pairs.append(current_pair)
                current_pair = {'question': line[2:].strip()}
            elif line.startswith('A:'):
                current_pair['answer'] = line[2:].strip()
                
        if current_pair:
            qa_pairs.append(current_pair)
            
        return qa_pairs
        
    def generate_hyde(self, query: str) -> str:
        """生成假设文档"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请生成一个假设的文档片段，该片段可能会完美回答以下查询。
这个假设文档将用于提高检索效果。"""),
            HumanMessage(content=query)
        ]
        
        return self.chat(messages)
        
    def rewrite_query(self, query: str) -> List[str]:
        """改写查询"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请用3种不同的方式改写以下查询，以提高检索效果。
改写时要保持原始意图，但使用不同的表达方式。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        return [q.strip() for q in response.split('\n') if q.strip()] 