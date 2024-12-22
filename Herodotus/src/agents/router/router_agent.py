from typing import Dict, Optional, List
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class RouterAgent(BaseAgent):
    """路由代理，负责任务分发和结果整合"""
    
    ROLE = """你是一个智能路由代理。
    
    你的主要职责是：
    1. 分析任务需求
    2. 确定需要使用的代理组合
    3. 规划代理调用顺序
    4. 整合多个代理的处理结果
    
    请确保合理分配任务并有效整合结果。"""
    
    def __init__(self, model_name: Optional[str] = None):
        super().__init__(model_name, streaming=False)
        self.registered_agents = {}
        
    def register_agents(self, agents: Dict[str, BaseAgent]) -> None:
        """注册可用的代理
        
        Args:
            agents: 代理字典，键为代理类型，值为代理实例
        """
        self.registered_agents = {k: v for k, v in agents.items() if v is not None}
        
    def analyze_task(self, task: str) -> Dict:
        """分析任务，确定需要使用的代理
        
        Args:
            task: 任务描述
            
        Returns:
            包含代理使用计划的字典
        """
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            
            可用的代理类型：
            - rag: RAG代理，用于文档处理和知识检索
            - tool: 工具代理，用于执行具体操作
            - memory: 记忆代理，用于管理对话历史
            
            请分析以下任务，确定：
            1. 需要使用哪些代理
            2. 代理的调用顺序
            3. 每个代理的具体任务
            
            返回JSON格式的分析结果。"""),
            HumanMessage(content=task)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def process(self, task: str, context: str = "") -> str:
        """处理任务，协调多个代理
        
        Args:
            task: 要处理的任务
            context: 上下文信息
            
        Returns:
            处理结果
        """
        # 分析任务
        plan = self.analyze_task(task)
        
        # 检查是否有可用的代理
        if not self.registered_agents:
            return "错误：没有注册任何代理。"
            
        results = []
        current_context = context
        
        # 按计划调用代理
        for step in plan.get("steps", []):
            agent_type = step.get("agent")
            if agent_type in self.registered_agents:
                agent = self.registered_agents[agent_type]
                result = agent.process(step.get("task", task), current_context)
                results.append({
                    "agent": agent_type,
                    "task": step.get("task", task),
                    "result": result
                })
                current_context = result
        
        # 如果只有一个结果，直接返回
        if len(results) == 1:
            return results[0]["result"]
            
        # 整合多个代理的结果
        return self.combine_results([r["result"] for r in results])
        
    def evaluate_results(self, task: str, results: List[Dict]) -> Dict:
        """评估处理结果
        
        Args:
            task: 原始任务
            results: 处理结果列表
            
        Returns:
            评估报告
        """
        messages = [
            SystemMessage(content=f"""{self.ROLE}
            
            请评估以下处理结果：
            1. 是否完成了原始任务
            2. 各个代理的贡献
            3. 结果的质量
            4. 可能的改进建议
            
            返回JSON格式的评估报告。"""),
            HumanMessage(content=f"""原始任务：{task}
            
            处理结果：
            {json.dumps(results, ensure_ascii=False, indent=2)}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response) 