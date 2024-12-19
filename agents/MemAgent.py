from typing import Dict, List
from ..base import BaseMemory
class MemoryAgent:
    """Manages different types of memory"""
    def __init__(self, short_term: BaseMemory, long_term: BaseMemory):
        self.short_term = short_term
        self.long_term = long_term
        
    def add_to_short_term(self, data: Dict[str, Any]):
        self.short_term.save_context(data, {})
        
    def add_to_long_term(self, data: Dict[str, Any]):
        self.long_term.save_context(data, {})


class BaseMemory(ABC):
    """Base abstract class for memory system"""
    
    @abstractmethod
    def add(self, data: Any) -> None:
        """Add memory"""
        pass
    
    @abstractmethod
    def get(self, query: Any) -> Any:
        """Get memory"""
        pass

class ShortTermMemory(BaseMemory):
    """Short-term memory implementation"""
    
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
    """Long-term memory implementation"""
    
    def __init__(self):
        self.memory = {}
    
    def add(self, key: str, data: Any) -> None:
        self.memory[key] = data
    
    def get(self, query: str) -> Any:
        return self.memory.get(query)