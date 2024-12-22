from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class RerankAgent(BaseAgent):
    """基于语言模型的重排序代理"""
    
    ROLE = """你是一个专门进行搜索结果重排序的AI助手。

你的主要职责是：
1. 分析查询需求
2. 评估结果质量
3. 确定排序标准
4. 优化结果顺序

请确保重排序后的结果更符合用户需求。"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化重排序代理
        
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
        
    def analyze_requirements(self, query: str) -> Dict:
        """分析排序需求"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请分析查询的排序需求：
1. 重要性权重
2. 时效性要求
3. 多样性需求
4. 专业度要求
5. 其他特殊要求

请以JSON格式返回分析结果。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def evaluate_result(self, query: str, result: Dict) -> Dict:
        """评估单个结果"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估该结果的各个方面：
1. 相关性(0-1)
2. 质量(0-1)
3. 完整性(0-1)
4. 可靠性(0-1)
5. 时效性(0-1)

请以JSON格式返回评估分数。"""),
            HumanMessage(content=f"""查询：
{query}

结果：
{json.dumps(result, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def get_weights(self, query: str) -> Dict:
        """获取排序权重"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请为该查询确定各个评估维度的权���：
1. 相关性权重
2. 质量权重
3. 完整性权重
4. 可靠性权重
5. 时效性权重

权重之和应为1。请以JSON格式返回权重配置。"""),
            HumanMessage(content=query)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def compare_results(self, query: str, result1: Dict, result2: Dict) -> int:
        """比较两个结果的优先级"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请比较两个结果的优先级。
返回：
1: 结果1更好
0: 相当
-1: 结果2更好

只返回数字，不要其他内容。"""),
            HumanMessage(content=f"""查询：
{query}

结果1：
{json.dumps(result1, ensure_ascii=False, indent=2)}

结果2：
{json.dumps(result2, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        try:
            return int(response.strip())
        except:
            return 0
            
    def rerank_results(self, query: str, results: List[Dict], weights: Dict = None) -> List[Dict]:
        """重排序结果"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请重新排序以下结果列表。
考虑：
1. 查询意图
2. 结果质量
3. 排序权重
4. 结果多���性

请以JSON数组格式返回重排序后的结果列表。"""),
            HumanMessage(content=f"""查询：
{query}

结果：
{json.dumps(results, ensure_ascii=False, indent=2)}

权重：
{json.dumps(weights, ensure_ascii=False, indent=2) if weights else "默认权重"}""")
        ]
        
        response = self.chat(messages)
        try:
            return json.loads(response)
        except:
            return results
            
    def evaluate_ranking(self, query: str, original_results: List[Dict], reranked_results: List[Dict]) -> Dict:
        """评估重排序效果"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估重排序的效果：
1. 相关性提升
2. 排序合理性
3. 多样性平衡
4. 用户满意度
5. 改进建议

请以JSON格式返回评估结果。"""),
            HumanMessage(content=f"""查询：
{query}

原始结果：
{json.dumps(original_results, ensure_ascii=False, indent=2)}

重排序结果：
{json.dumps(reranked_results, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def optimize_diversity(self, query: str, results: List[Dict]) -> List[Dict]:
        """优化结果多样性"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请优化结果的多样性：
1. 避免冗余
2. 覆盖不同角度
3. 平衡相关性
4. 保持连贯性

请以JSON数组格式返回优化后的结果列表。"""),
            HumanMessage(content=f"""查询：
{query}

结果：
{json.dumps(results, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        try:
            return json.loads(response)
        except:
            return results 