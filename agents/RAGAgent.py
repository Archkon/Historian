from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..base import BaseAgent

class DataAgent(BaseAgent):
    """数据处理Agent"""
    
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