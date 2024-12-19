from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..base import BaseAgent
class RAGAgent(BaseAgent):
    """Handles RAG operations"""
    def __init__(self, llm_chain: LLMChain):
        self.llm_chain = llm_chain
        
    def process(self, query: str) -> str:
        return self.llm_chain.run(query)

class DataAgent(BaseAgent):
    """Data Processing Agent"""
    
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def run(self, file_path: str) -> List[Document]:
        # 加载文档
        loader = TextLoader(file_path)
        documents = loader.load()
        
        # 分块处理
        return self.text_splitter.split_documents(documents) 


# class DataAgent(RAGAgent):
#     """Handles data preprocessing tasks"""
#     def __init__(self, text_splitter: TextSplitter):
#         self.text_splitter = text_splitter
        
#     def process(self, documents: List[str]) -> List[str]:
#         return self.text_splitter.split_documents(documents)
    
class RewriteAgent(RAGAgent):
    """Handles text rewriting tasks"""
    def __init__(self, prompt: PromptTemplate):
        self.prompt = prompt

class EmbeddingAgent(BaseAgent):
    """Handles embedding operations"""
    def __init__(self, embedding_model: Embeddings):
        self.embedding_model = embedding_model
        
    def process(self, texts: List[str]) -> List[List[float]]:
        return self.embedding_model.embed_documents(texts)

class RetrievalAgent(BaseAgent):
    """Handles retrieval operations"""
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
    def process(self, query: str, k: int = 4) -> List[str]:
        return self.vector_store.similarity_search(query, k=k)
