from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import json
import logging

# 加载环境变量
load_dotenv()

class BaseAgent:
    """基础代理类"""
    
    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化基础代理
        
        Args:
            model_name: 模型名称
            api_key: OpenAI API密钥
            api_base: OpenAI API基础URL
            streaming: 是否启用流式输出
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.streaming = streaming
        
        # 设置日志记录器
        self.logger = logging.getLogger(self.__class__.__name__)
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        # 从环境变量获取配置
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        # 设置回调
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]) if self.streaming else None
        
        # 初始化语言模型
        self.llm = ChatOpenAI(
            model_name=model_name,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=self.streaming,
            callback_manager=callback_manager
        )
        
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=self.api_key,
            openai_api_base=self.api_base
        )
        
    def chat(self, messages):
        """与语言模型交互"""
        return self.llm.invoke(messages).content
        
    def process(self, task: str, context: str = "") -> str:
        """处理任务，支持上下文传递
        
        Args:
            task: 要处理的任务
            context: 上下文信息，可能来自其他代理的处理结果
            
        Returns:
            处理结果
        """
        messages = [
            SystemMessage(content=f"""你是一个智能代理。
            
            当前任务：{task}
            
            如果提供了上下文信息，请在处理任务时考虑这些信息。
            如果上下文为空，则直接处理任务。
            
            请确保输出结果清晰、准确。"""),
            HumanMessage(content=f"上下文信息：{context}" if context else task)
        ]
        
        return self.chat(messages)
        
    def update_config(self, config: Dict[str, Any]) -> None:
        """更新代理配置
        
        Args:
            config: 新的配置信息
        """
        # 更新语言模型配置
        self.llm = ChatOpenAI(
            model_name=config.get("model", self.llm.model_name),
            temperature=config.get("temperature", self.llm.temperature),
            max_tokens=config.get("max_tokens", self.llm.max_tokens),
            streaming=config.get("stream_output", self.llm.streaming)
        )
        
    def combine_results(self, results: list) -> str:
        """合并多个处理结果
        
        Args:
            results: 处理结果列表
            
        Returns:
            合并后的结果
        """
        messages = [
            SystemMessage(content="""你是一个结果整合专家。
            
            请将多个处理结果整合成一个连贯的输出。
            需要：
            1. 去除重复信息
            2. 保持逻辑顺序
            3. 确保内容完整
            4. 语言通顺自然"""),
            HumanMessage(content=f"请整合以下结果：\n\n{json.dumps(results, ensure_ascii=False, indent=2)}")
        ]
        
        return self.chat(messages)