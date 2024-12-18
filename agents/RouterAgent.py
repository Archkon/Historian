from typing import Dict, Type
from ..base import BaseAgent

class RouterAgent(BaseAgent):
    """路由Agent"""
    
    def __init__(self):
        self.routes: Dict[str, BaseAgent] = {}
    
    def register(self, name: str, agent: BaseAgent) -> None:
        """注册一个agent"""
        self.routes[name] = agent
    
    def run(self, route_name: str, *args, **kwargs) -> Any:
        """路由到指定的agent"""
        if route_name not in self.routes:
            raise KeyError(f"未找到路由: {route_name}")
        return self.routes[route_name].run(*args, **kwargs) 