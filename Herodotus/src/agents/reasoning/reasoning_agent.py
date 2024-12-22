from typing import Dict, Any, List
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class ReasoningAgent(BaseAgent):
    """实现各种推理技巧的代理"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name, streaming=False)
        self.reasoning_techniques = {
            "zero_shot": False,
            "few_shot": False,
            "one_shot": False,
            "cot": False,
            "least_to_most": False,
            "self_consistency": False,
            "react": False,
            "reflection": False,
            "tot": False
        }
        
    def process(self, task: str, context: str = "") -> str:
        """处理任务,应用选定的推理技巧"""
        messages = []
        
        # 构建系统提示
        system_prompt = "你是一个专门进行推理的AI助手。请根据以下推理技巧分析问题并给出答案:\n"
        if self.reasoning_techniques["zero_shot"]:
            system_prompt += "- 零样本推理:直接根据问题进行推理,不需要任何示例\n"
        if self.reasoning_techniques["few_shot"]:
            system_prompt += "- 少样本推理:参考少量相似示例进行推理\n"
        if self.reasoning_techniques["one_shot"]:
            system_prompt += "- 单样本推理:参考一个相似示例进行推理\n"
        if self.reasoning_techniques["cot"]:
            system_prompt += "- 思维链推理:一步一步展示推理过程\n"
        if self.reasoning_techniques["least_to_most"]:
            system_prompt += "- 最少到最多推理:从最简单的子问题开始,逐步解决复杂问题\n"
        if self.reasoning_techniques["self_consistency"]:
            system_prompt += "- 自洽性推理:生成多个推理路径并选择最一致的结果\n"
        if self.reasoning_techniques["react"]:
            system_prompt += "- ReAct推理:思考-行动-观察交替进行\n"
        if self.reasoning_techniques["reflection"]:
            system_prompt += "- 反思推理:对推理过程进行反思和改进\n"
        if self.reasoning_techniques["tot"]:
            system_prompt += "- 思维树推理:生成多个推理分支并选择最优路径\n"
            
        messages.append(SystemMessage(content=system_prompt))
        
        # 添加任务和上下文
        task_prompt = f"任务: {task}\n"
        if context:
            task_prompt += f"上下文: {context}\n"
        messages.append(HumanMessage(content=task_prompt))
        
        # 获取响应
        response = self.chat(messages)
        
        return response
        
    def zero_shot_reasoning(self, task: str) -> str:
        """零样本推理"""
        messages = [
            SystemMessage(content="请直接根据问题进行推理,不需要任何示例。"),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def few_shot_reasoning(self, task: str, examples: List[Dict[str, str]]) -> str:
        """少样本推理"""
        messages = [
            SystemMessage(content="请参考以下示例进行推理:")
        ]
        
        # 添加示例
        for example in examples:
            messages.append(HumanMessage(content=example["question"]))
            messages.append(SystemMessage(content=example["answer"]))
            
        messages.append(HumanMessage(content=task))
        return self.chat(messages)
        
    def chain_of_thought(self, task: str) -> str:
        """思维链推理"""
        messages = [
            SystemMessage(content="请一步一步地展示你的推理过程:"),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def least_to_most(self, task: str) -> str:
        """最少到最多推理"""
        messages = [
            SystemMessage(content="""请按照以下步骤进行推理:
            1. 将问题分解为多个简单的子问题
            2. 从最简单的子问题开始解决
            3. 逐步解决更复杂的子问题
            4. 最后得出完整的解决方案"""),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def self_consistency(self, task: str, num_paths: int = 3) -> str:
        """自洽性推理"""
        messages = [
            SystemMessage(content=f"""请生成{num_paths}个不同的推理路径,然后选择最一致的结果。
            对于每个路径:
            1. 说明推理步骤
            2. 给出结论
            最后:
            1. 比较不同路径的结论
            2. 选择最一致的结果"""),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def react(self, task: str) -> str:
        """ReAct推理"""
        messages = [
            SystemMessage(content="""请按照以下格式进行推理:
            思考: 分析当前情况
            行动: 采取具体行动
            观察: 记录行动结果
            重复以上步骤直到得出最终结论"""),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def reflection(self, task: str) -> str:
        """反思推理"""
        messages = [
            SystemMessage(content="""请按照以下步骤进行推理:
            1. 初步分析和推理
            2. 反思推理过程中的假设和潜在问题
            3. 根据反思调整推理过程
            4. 得出改进后的结论"""),
            HumanMessage(content=task)
        ]
        return self.chat(messages)
        
    def tree_of_thoughts(self, task: str, max_branches: int = 3, max_depth: int = 3) -> str:
        """思维树推理"""
        messages = [
            SystemMessage(content=f"""请构建一个思维树进行推理:
            1. 生成最多{max_branches}个初始思路分支
            2. 对每个分支进行最多{max_depth}层的深入推理
            3. 评估每条路径的可行性
            4. 选择最优路径作为最终结论"""),
            HumanMessage(content=task)
        ]
        return self.chat(messages) 