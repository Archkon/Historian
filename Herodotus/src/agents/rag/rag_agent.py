from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
from .data_agent import DataAgent
from .rewrite_agent import RewriteAgent
from .embedding_agent import EmbeddingAgent
from .database_agent import DatabaseAgent
from .retrieval_agent import RetrievalAgent
from .rerank_agent import RerankAgent

class RAGAgent(BaseAgent):
    """基于语言模型的RAG代理"""
    
    ROLE = """你是一个专门处理文档分析和知识检索的AI助手。
    
你的主要职责是：
1. 理解和分析文档内容
2. 回答关于文档的问题
3. 总结文档要点
4. 提取文档中的关键信息

请基于检索到的相关文档内容，以专业、准确的方式回答问题。
如果文档中没有相关信息，请明确指出。"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True,
                 use_embedding: bool = True,
                 use_database: bool = True,
                 use_retrieval: bool = True,
                 use_rerank: bool = True):
        """初始化RAG代理
        
        Args:
            model_name: 模型名称
            api_key: OpenAI API密钥
            api_base: OpenAI API基础URL
            streaming: 是否启用流式输出
            use_embedding: 是否使用嵌入
            use_database: 是否使用数据库
            use_retrieval: 是否使用检索
            use_rerank: 是否使用重排序
        """
        super().__init__(model_name=model_name, 
                        api_key=api_key, 
                        api_base=api_base,
                        streaming=streaming)
        
        self.use_embedding = use_embedding
        self.use_database = use_database
        self.use_retrieval = use_retrieval
        self.use_rerank = use_rerank
        
        # 初始化子组件
        if self.use_embedding:
            from .embedding_agent import EmbeddingAgent
            self.embedding_agent = EmbeddingAgent(model_name=model_name, api_key=api_key, api_base=api_base)
            
        if self.use_database:
            from .database_agent import DatabaseAgent
            self.database_agent = DatabaseAgent(model_name=model_name, api_key=api_key, api_base=api_base)
            
        if self.use_retrieval:
            from .retrieval_agent import RetrievalAgent
            self.retrieval_agent = RetrievalAgent(model_name=model_name, api_key=api_key, api_base=api_base)
            
        if self.use_rerank:
            from .rerank_agent import RerankAgent
            self.rerank_agent = RerankAgent(model_name=model_name, api_key=api_key, api_base=api_base)
        
    def load_documents(self, file_paths: List[str]) -> None:
        """加载并处理文档"""
        try:
            # 1. 数据处理
            processed_docs = []
            for path in file_paths:
                result = self.data_agent.process_document(path)
                processed_docs.extend(result["texts"])
                
            # 2. 文本重写（生成问答对）
            enhanced_texts = []
            for doc in processed_docs:
                qa_pairs = self.rewrite_agent.text_to_qa(doc.page_content)
                enhanced_texts.extend([qa["question"] for qa in qa_pairs])
                enhanced_texts.extend([qa["answer"] for qa in qa_pairs])
                
            # 3. 语义分析
            semantic_representations = self.embedding_agent.embed_texts(enhanced_texts)
            
            # 4. 存储到知识库
            for text, semantic in zip(enhanced_texts, semantic_representations):
                self.database_agent.add_knowledge(text, semantic)
            
        except Exception as e:
            raise ValueError(f"文档加载失败: {str(e)}")
            
    def query(self, question: str) -> str:
        """查询知识库获取答案"""
        try:
            # 1. 重写查询
            rewritten_queries = self.rewrite_agent.rewrite_query(question)
            
            # 2. 获取检索策略
            strategy = self.retrieval_agent.get_strategy(question)
            
            # 3. 执行检索
            all_results = []
            for query in rewritten_queries:
                results = self.database_agent.search_knowledge(
                    query,
                    top_k=strategy["params"]["k"]
                )
                all_results.extend(results)
                
            # 4. 过滤结果
            filtered_results = self.retrieval_agent.filter_results(
                all_results,
                min_score=strategy["params"]["min_relevance"]
            )
            
            # 5. 重排序结果
            weights = self.rerank_agent.get_weights(question)
            reranked_results = self.rerank_agent.rerank_results(
                question,
                filtered_results,
                weights
            )
            
            # 6. 生成最终答案
            context = "\n\n".join([r["content"] for r in reranked_results[:3]])
            
            messages = [
                SystemMessage(content=self.ROLE),
                HumanMessage(content=f"""基于以下文档内容回答问题:

文档内容:
{context}

问题:
{question}""")
            ]
            
            return self.chat(messages)
            
        except Exception as e:
            raise ValueError(f"查询失败: {str(e)}")
            
    def evaluate_pipeline(self, question: str, answer: str) -> Dict:
        """评估整个管道的性能"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估整个RAG管道的性能。"""),
            HumanMessage(content=f"""查询: {question}

生成的答案:
{answer}

请评估以下方面：
1. 答案的相关性
2. 答案的准确性
3. 答案的完整性
4. 检索效果
5. 改进建议""")
        ]
        
        response = self.chat(messages)
        return response