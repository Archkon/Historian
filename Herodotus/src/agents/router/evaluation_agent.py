from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class EvaluationAgent(BaseAgent):
    """评估代理"""
    
    ROLE = """你是一个专门进行质量评估的AI助手。

你的主要职责是：
1. 评估回答的质量和相关性
2. 检查信息的准确性
3. 评估输出的完整性
4. 提供改进建议

请以JSON格式返回评估结果：
{
    "score": 0-100,
    "relevance": 0-100,
    "accuracy": 0-100,
    "completeness": 0-100,
    "suggestions": ["建议1", "建议2"]
}"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name, streaming=False)
        
    def evaluate_response(self, query: str, response: str, context: str = None) -> Dict:
        """评估回答"""
        messages = [
            SystemMessage(content=self.ROLE),
            HumanMessage(content=f"""请评估以下回答的质量：

查询：
{query}

回答：
{response}

{'参考上下文：\n' + context if context else ''}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def evaluate_relevance(self, query: str, documents: List[str]) -> List[Dict]:
        """评估文档相关性"""
        results = []
        for doc in documents:
            messages = [
                SystemMessage(content=f"""{self.ROLE}
请评估以下文档与查询的相关性。"""),
                HumanMessage(content=f"""查询：
{query}

文档内容：
{doc}""")
            ]
            
            response = self.chat(messages)
            results.append(json.loads(response))
            
        return results
        
    def get_improvement_suggestions(self, content: str) -> List[str]:
        """获取改进建议"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请分析以下内容并提供具体的改进建议。
建议应该具体、可操作，并且有助于提高内容质量。"""),
            HumanMessage(content=content)
        ]
        
        response = self.chat(messages)
        result = json.loads(response)
        return result["suggestions"] 