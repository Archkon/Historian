class ReasoningAgent(BaseAgent):
    """Handles reasoning and decision making"""
    def __init__(self, llm: BaseLLM, memory_manager: Optional[MemoryManager] = None):
        self.llm = llm
        self.memory_manager = memory_manager
        
    def process(self, query: str, context: List[str]) -> str:
        prompt = self._build_cot_prompt(query, context)
        return self.llm(prompt)
        
    def _build_cot_prompt(self, query: str, context: List[str]) -> str:
        return f"""Let's solve this step by step:
Context: {' '.join(context)}
Question: {query}
Let's think about this step by step:
1)"""