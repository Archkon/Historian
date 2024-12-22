from typing import List, Dict, Any, Callable
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.tools import Tool
import json

class ToolAgent(BaseAgent):
    """工具代理"""
    
    ROLE = """你是一个专门执行具体任务的工具代理。
    
你可以使用以下工具来完成任务：
{available_tools}

你的职责是：
1. 理解用户的任务需求
2. 选择合适的工具
3. 正确使用工具完成任务
4. 返回执行结果

请按以下格式返回你的决定：
{
    "tool": "工具名称",
    "parameters": {
        "参数1": "值1",
        "参数2": "值2"
    }
}"""

    def __init__(self, model_name: str = "gpt-3.5-turbo", streaming: bool = True):
        super().__init__(model_name, streaming)
        self.tools = {}
        
    def add_tool(self, name: str, func: Callable, description: str):
        """添加新工具"""
        self.tools[name] = {
            "func": func,
            "description": description
        }
        
    def execute(self, task: str) -> str:
        """执行任务"""
        if not self.tools:
            raise ValueError("请先添加工具!")
            
        # 构建工具描述
        tools_desc = "\n".join([
            f"- {name}: {tool['description']}"
            for name, tool in self.tools.items()
        ])
        
        # 构建提示
        messages = [
            SystemMessage(content=self.ROLE.format(available_tools=tools_desc)),
            HumanMessage(content=task)
        ]
        
        # 获取模型决策
        response = self.chat(messages)
        try:
            decision = json.loads(response)
            tool_name = decision["tool"]
            parameters = decision["parameters"]
            
            if tool_name not in self.tools:
                raise ValueError(f"未知的工具: {tool_name}")
                
            # 执行工具
            result = self.tools[tool_name]["func"](**parameters)
            return str(result)
            
        except json.JSONDecodeError:
            raise ValueError("工具代理返回了无效的JSON格式")
        except KeyError as e:
            raise ValueError(f"工具代理返回的数据缺少必要字段: {str(e)}")
        except Exception as e:
            raise ValueError(f"工具执行出错: {str(e)}") 