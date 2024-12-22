from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.vectorstores import FAISS
import json
import numpy as np

class DatabaseAgent(BaseAgent):
    """基于语言模型的知识存储代理"""
    
    ROLE = """你是一个专门管理知识的AI助手。

你的主要职责是：
1. 组织和索引知识
2. 管理知识结构
3. 提供知识检索
4. 维护知识一致性

请以JSON格式返回分析结果：
{
    "knowledge_structure": {
        "categories": ["类别1", "类别2"],
        "relationships": ["关系1", "关系2"]
    },
    "importance": 0-1,
    "metadata": {
        "source": "来源",
        "timestamp": "时间戳"
    }
}"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化数据库代理
        
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
                        
        # 初始化向量数据库
        self.vector_store = None
        
    def add_knowledge(self, text: str, metadata: Dict = None) -> None:
        """添加知识到存储"""
        # 生成文本的嵌入向量
        embedding = self.embeddings.embed_query(text)
        
        # 如果向量数据库不存在，创建一个新的
        if self.vector_store is None:
            self.vector_store = FAISS.from_embeddings(
                [embedding],
                [text],
                self.embeddings,
                metadatas=[metadata] if metadata else None
            )
        else:
            # 添加到现有数据库
            self.vector_store.add_embeddings(
                [embedding],
                [text],
                [metadata] if metadata else None
            )
        
    def search_knowledge(self, query: str, top_k: int = 3) -> List[Dict]:
        """搜索相关知识"""
        if self.vector_store is None:
            return []
            
        # 使用向量数据库进行相似度搜索
        results = self.vector_store.similarity_search_with_score(
            query,
            k=top_k
        )
        
        # 格式化结果
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)  # 转换numpy.float64为Python float
            })
            
        return formatted_results 