from pyclbr import Class
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate

class BaseAgent(ABC):
    """Base class for all agents"""
    @abstractmethod
    def process(self, *args, **kwargs):
            pass