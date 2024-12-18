from typing import Dict, List
from ..base import BaseMemory

class BaseMemory(ABC):
    """记忆系统的基础抽象类"""
    
    @abstractmethod
    def add(self, data: Any) -> None:
        """添加记忆"""
        pass
    
    @abstractmethod
    def get(self, query: Any) -> Any:
        """获取记忆"""
        pass

class ShortTermMemory(BaseMemory):
    """短期记忆实现"""
    
    def __init__(self, max_items=10):
        self.memory = []
        self.max_items = max_items
    
    def add(self, data: Any) -> None:
        self.memory.append(data)
        if len(self.memory) > self.max_items:
            self.memory.pop(0)
    
    def get(self, query: Any = None) -> List:
        return self.memory

class LongTermMemory(BaseMemory):
    """长期记忆实现"""
    
    def __init__(self):
        self.memory = {}
    
    def add(self, key: str, data: Any) -> None:
        self.memory[key] = data
    
    def get(self, query: str) -> Any:
        return self.memory.get(query)