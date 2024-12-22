from typing import List, Dict, Any
from ..base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage
import json
import os

class DataAgent(BaseAgent):
    """基于语言模型的数据处理代理"""
    
    ROLE = """你是一个专门处理和分析文本数据的AI助手。

你的主要职责是：
1. 读取和理解文档内容
2. 清洗和标准化文本
3. 将长文本分割成语义完整的片段
4. 提取和组织关键信息

请确保处理后的文本保持语义完整性和连贯性。"""

    CHUNK_PROMPT = """请将以下文本分割成多个语义完整的片段。
每个片段应该：
1. 包含完整的上下文
2. 长度适中（约500-1000字）
3. 保持语义连贯性
4. 避免跨段落的概念割裂

请以JSON格式返回分割结果：
{
    "chunks": [
        {
            "content": "片段内容",
            "summary": "片段摘要",
            "key_points": ["要点1", "要点2"]
        }
    ]
}"""

    def __init__(self, 
                 model_name: str = "gpt-3.5-turbo",
                 api_key: str = None,
                 api_base: str = None,
                 streaming: bool = True):
        """初始化数据代理
        
        Args:
            model_name: 模型名称
            api_key: OpenAI API密钥
            api_base: OpenAI API基础URL
            streaming: 是否启用流式输出
        """
        super().__init__(model_name=model_name, 
                        api_key=api_key, 
                        api_base=api_base,
                        streaming=streaming)
        
    def read_file(self, file_path: str) -> str:
        """读取文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    def clean_text(self, text: str) -> str:
        """清洗文本"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请清洗和标准化以下文本，包括：
1. 删除无意义的字符和空白
2. 修正明显的格式问题
3. 统一标点符号
4. 保持段落结构

只返回清洗后的文本，不要其他内容。"""),
            HumanMessage(content=text)
        ]
        
        return self.chat(messages)
        
    def split_text(self, text: str) -> List[Dict]:
        """分割文本"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}\n{self.CHUNK_PROMPT}"""),
            HumanMessage(content=text)
        ]
        
        response = self.chat(messages)
        try:
            result = json.loads(response)
            return result["chunks"]
        except:
            # 如果解析失败，将整个文本作为一个片段返回
            return [{
                "content": text,
                "summary": "完整文档",
                "key_points": ["文档内容"]
            }]
            
    def analyze_chunk(self, chunk: str) -> Dict:
        """分析文本片段"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请分析以下文本片段，提供：
1. 主要主题
2. 关键概念
3. 重要实体
4. 文本类型
5. 复杂度评估

请以JSON格式返回分析结果。"""),
            HumanMessage(content=chunk)
        ]
        
        response = self.chat(messages)
        return json.loads(response)
        
    def process_document(self, file_path: str) -> Dict:
        """处理文档"""
        try:
            # 读取文件
            text = self.read_file(file_path)
            
            # 清洗文本
            cleaned_text = self.clean_text(text)
            
            # 分割文本
            chunks = self.split_text(cleaned_text)
            
            # 分析每个片段
            processed_chunks = []
            for chunk in chunks:
                analysis = self.analyze_chunk(chunk["content"])
                processed_chunks.append({
                    **chunk,
                    "analysis": analysis
                })
                
            return {
                "texts": processed_chunks,
                "metadata": {
                    "file_path": file_path,
                    "file_name": os.path.basename(file_path),
                    "chunk_count": len(processed_chunks)
                }
            }
            
        except Exception as e:
            raise ValueError(f"文档处理失败: {str(e)}")
            
    def merge_chunks(self, chunks: List[Dict]) -> str:
        """合并文本片段"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请将以下文本片段合并成一个连贯的文档。
确保：
1. 保持逻辑流畅
2. 添加必要的过渡
3. 消除重复内容
4. 统一行文风格

只返回合并后的文本，不要其他内容。"""),
            HumanMessage(content=json.dumps([chunk["content"] for chunk in chunks], ensure_ascii=False, indent=2))
        ]
        
        return self.chat(messages)
        
    def evaluate_quality(self, text: str) -> Dict:
        """评估文本质量"""
        messages = [
            SystemMessage(content=f"""{self.ROLE}
请评估以下文本的质量，包括：
1. 可读性
2. 连贯性
3. 完整性
4. 格式规范性
5. 信息密度

请以JSON格式返回评估结果。"""),
            HumanMessage(content=text)
        ]
        
        response = self.chat(messages)
        return json.loads(response)