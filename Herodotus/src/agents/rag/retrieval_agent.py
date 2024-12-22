from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class RetrievalAgent(BaseAgent):
    """基于语言模型的检索代理"""
    
    ROLE = """你是一个专门进行文档检索的AI助手。

你的主要职责是：
1. 分析查询意图
2. 设计检索策略
3. 评估检索结果
4. 优化检索效果

请确保检索结果与查询意图高度相关。"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化检索代理
        
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
        
    def analyze_query(self, query: str) -> Dict:
        """分析查询意图"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请分析以下查询的意图：
1. 查询类型
2. 关键概念
3. 期望结果
4. 可能的扩展

请以JSON格式返回分析结果。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def get_strategy(self, query: str) -> Dict:
        """获取检索策略"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请为以下查询设计检索策略：
1. 检索方法
2. 关键词扩展
3. 相关度阈值
4. 结果数量
5. 排序方式

请以JSON格式返回策略。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def evaluate_relevance(self, query: str, document: str) -> float:
        """评估文档相关性"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估文档与查询的相关性，返回0-1之间的分数。
1表示完全相关，0表示完全不相关。
只返回数字，不���其他内容。"""),
            HumanMessage(content=f"""查询：
{query}

文档：
{document}""")
        ]
        
        response = self.chat(messages)
        try:
            return float(response.strip())
        except:
            return 0.0
            
    def filter_results(self, results: List[Dict], min_score: float = 0.5) -> List[Dict]:
        """过滤检索结果"""
        filtered = []
        for result in results:
            if result.get("score", 0) >= min_score:
                filtered.append(result)
        return filtered
        
    def expand_query(self, query: str) -> List[str]:
        """扩展查询"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请为以下查询生成多个相关的扩展查询。
考虑：
1. 同义词替换
2. 概念扩展
3. 上下位概念
4. 相关主题

请以JSON数组格式返回扩展查询列表。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        try:
            return json.loads(response)
        except:
            return [query]
            
    def optimize_results(self, query: str, results: List[Dict]) -> List[Dict]:
        """优化检索结果"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请优化以下检索结果：
1. 去除冗余
2. 补充缺失
3. 调整顺序
4. 确保多样性

请以JSON格式返回优化后的结果列表。"""),
            HumanMessage(content=f"""查询：
{query}

检索结果：
{json.dumps(results, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        try:
            return json.loads(response)
        except:
            return results
            
    def evaluate_strategy(self, query: str, strategy: Dict, results: List[Dict]) -> Dict:
        """评估检索策略"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估检索策略的效果：
1. 结果相关性
2. 结果覆盖度
3. 结果多样性
4. 策略适用性
5. 改进建议

请以JSON格式返回评估结果。"""),
            HumanMessage(content=f"""查询：
{query}

策略：
{json.dumps(strategy, ensure_ascii=False, indent=2)}

检索结果：
{json.dumps(results, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response) 