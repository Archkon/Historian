from pyclbr import Class
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from langchain.llms.base import BaseLLM
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.base import VectorStore
from langchain.text_splitter import TextSplitter
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import BaseMemory

class BaseAgent(ABC):
    """Base class for all agents"""
    @abstractmethod
    def process(self, *args, **kwargs):
        pass
class RAGAgent(BaseAgent):
    """Handles RAG operations"""
    def __init__(self, llm_chain: LLMChain):
        self.llm_chain = llm_chain
        
    def process(self, query: str) -> str:
        return self.llm_chain.run(query)

class DataAgent(RAGAgent):
    """Handles data preprocessing tasks"""
    def __init__(self, text_splitter: TextSplitter):
        self.text_splitter = text_splitter
        
    def process(self, documents: List[str]) -> List[str]:
        return self.text_splitter.split_documents(documents)
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

class MemoryManager:
    """Manages different types of memory"""
    def __init__(self, short_term: BaseMemory, long_term: BaseMemory):
        self.short_term = short_term
        self.long_term = long_term
        
    def add_to_short_term(self, data: Dict[str, Any]):
        self.short_term.save_context(data, {})
        
    def add_to_long_term(self, data: Dict[str, Any]):
        self.long_term.save_context(data, {})

class ReasoningAgent(BaseAgent):
    """Handles reasoning and decision making"""
    def __init__(self, llm: BaseLLM, memory_manager: Optional[MemoryManager] = None):
        self.llm = llm
        self.memory_manager = memory_manager
        
    def process(self, query: str, context: List[str]) -> str:
        prompt = self._build_cot_prompt(query, context)
        return self.llm(prompt)
        
    def _build_cot_prompt(self, query: str, context: List[str]) -> str:
        return f"""Let's solve this step by step:
Context: {' '.join(context)}
Question: {query}
Let's think about this step by step:
1)"""

class RouterAgent:
    """Routes requests to appropriate agents"""
    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
        
    def route(self, task_type: str, *args, **kwargs):
        if task_type in self.agents:
            return self.agents[task_type].process(*args, **kwargs)
        raise ValueError(f"No agent available for task type: {task_type}")