from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json

class PromptAgent(BaseAgent):
    """提示代理"""
    
    ROLE = """你是一个专门优化提示的AI助手。

你的主要职责是：
1. 根据任务生成最佳提示
2. 优化现有提示
3. 为不同场景定制提示
4. 提供提示改进建议

请以JSON格式返回提示：
{
    "system_prompt": "系统角色设定",
    "task_prompt": "具体任务描述",
    "format_prompt": "期望输出格式",
    "examples": ["示例1", "示例2"]
}"""

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        super().__init__(model_name, streaming=False)
        
    def generate_prompt(self, task: str, context: str = None) -> Dict:
        """生成提示"""
        messages = [
            SystemMessage(content=self.ROLE),
            HumanMessage(content=f"""请为以下任务生成最佳提示：

任务描述：
{task}

{'参考上下文：\n' + context if context else ''}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def optimize_prompt(self, original_prompt: str, feedback: str = None) -> Dict:
        """优化提示"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请优化以下提示，使其更加有效。"""),
            HumanMessage(content=f"""原始提示：
{original_prompt}

{'优化反馈：\n' + feedback if feedback else ''}""")
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def generate_examples(self, prompt: str, num_examples: int = 3) -> List[Dict]:
        """生成示例"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请为以下提示生成{num_examples}个示例。
示例应该展示提示的最佳使用方式。"""),
            HumanMessage(content=prompt)
        ]
        
        response = self.chat(messages)
        result = json.loads(response)
        return result["examples"] 