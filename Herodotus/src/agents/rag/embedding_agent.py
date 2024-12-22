from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class EmbeddingAgent(BaseAgent):
    """基于语言模型的嵌入代理"""
    
    ROLE = """你是一个专门进行语义理解和表示的AI助手。

你的主要职责是：
1. 理解文本的语义内容
2. 提取关键概念和主题
3. 生成语义表示
4. 评估语义相似度

请以JSON格式返回语义分析结果：
{
    "key_concepts": ["概念1", "概念2"],
    "main_topics": ["主题1", "主题2"],
    "semantic_summary": "语义概要",
    "importance_score": 0-1
}"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化嵌入代理
        
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
        
    def analyze_text(self, text: str) -> Dict:
        """分析文本语义"""
        messages = [
            SystemMessage(content=self.ROLE),
            HumanMessage(content=f"""请分析以下文本的语义内容：

{text}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def compare_texts(self, text1: str, text2: str) -> float:
        """比较两段文本的语义相似度"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请分析以下两段文本的语义相似度，返回0-1之间的分数。
1表示完全相似，0表示完全不相关。
只返回数字，不要其他内容。"""),
            HumanMessage(content=f"""文本1：
{text1}

文本2：
{text2}""")
        ]
        
        response = self.chat(messages)
        try:
            return float(response.strip())
        except:
            return 0.0
        
    def embed_texts(self, texts: List[str]) -> List[Dict]:
        """生成文本的语义表示"""
        # 使用OpenAI的嵌入模型生成向量
        embeddings = self.embeddings.embed_documents(texts)
        
        # 分析文本语义
        results = []
        for text, embedding in zip(texts, embeddings):
            analysis = self.analyze_text(text)
            results.append({
                "text": text,
                "embedding": embedding,
                "analysis": analysis
            })
        return results
        
    def find_similar(self, query: str, texts: List[str], top_k: int = 3) -> List[Dict]:
        """查找语义相似的文本"""
        # 生成查询的嵌入向量
        query_embedding = self.embeddings.embed_query(query)
        
        # 生成所有文本的嵌入向量
        text_embeddings = self.embeddings.embed_documents(texts)
        
        # 计算相似度
        similarities = []
        for text, embedding in zip(texts, text_embeddings):
            # 计算余弦相似度
            similarity = self.compute_cosine_similarity(query_embedding, embedding)
            similarities.append({
                "text": text,
                "score": similarity
            })
            
        # 按相似度排序
        similarities.sort(key=lambda x: x["score"], reverse=True)
        return similarities[:top_k]
        
    def evaluate_similarity(self, query: str, result: Dict) -> Dict:
        """评估检索结果的相关性"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估检索结果与查询的相关性。返回JSON格式：
{{
    "relevance_score": 0-1,
    "explanation": "相关性解释"
}}"""),
            HumanMessage(content=f"""查询：
{query}

检索结果：
{result["text"]}

相似度分数：{result["score"]}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response) 

    def compute_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 * norm2 != 0 else 0.0 