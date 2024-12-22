import argparse
import os
from dotenv import load_dotenv
from agents.rag.rag_agent import RAGAgent
from agents.tools.tool_agent import ToolAgent
from agents.memory.memory_agent import MemoryAgent
from agents.router.router_agent import RouterAgent
from agents.reasoning.reasoning_agent import ReasoningAgent

def main():
    # 加载环境变量
    load_dotenv()
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="Historian CLI工具")
    
    # 添加基本参数
    parser.add_argument("task", help="要执行的任务")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="要使用的模型名称")
    parser.add_argument("--temperature", type=float, default=0.7, help="生成温度")
    parser.add_argument("--max-tokens", type=int, default=2000, help="最大令牌数")
    
    # 添加代理选择参数
    parser.add_argument("--use-rag", action="store_true", help="使用RAG代理")
    parser.add_argument("--use-tool", action="store_true", help="使用工具代理")
    parser.add_argument("--use-memory", action="store_true", help="使用记忆代理")
    parser.add_argument("--use-router", action="store_true", help="使用路由代理")
    parser.add_argument("--use-reasoning", action="store_true", help="使用推理代理")
    
    # 添加推理技巧选择参数
    parser.add_argument("--zero-shot", action="store_true", help="使用零样本推理")
    parser.add_argument("--few-shot", action="store_true", help="使用少样本推理")
    parser.add_argument("--one-shot", action="store_true", help="使用单样本推理")
    parser.add_argument("--cot", action="store_true", help="使用思维链推理")
    parser.add_argument("--least-to-most", action="store_true", help="使用最少到最多推理")
    parser.add_argument("--self-consistency", action="store_true", help="使用自洽性推理")
    parser.add_argument("--react", action="store_true", help="使用ReAct推理")
    parser.add_argument("--reflection", action="store_true", help="使用反思推理")
    parser.add_argument("--tot", action="store_true", help="使用思维树推理")
    
    args = parser.parse_args()
    
    try:
        # 初始化代理
        agents = []
        if args.use_rag:
            agents.append(RAGAgent(model_name=args.model))
        if args.use_tool:
            agents.append(ToolAgent(model_name=args.model))
        if args.use_memory:
            agents.append(MemoryAgent(model_name=args.model))
        if args.use_router:
            router = RouterAgent(model_name=args.model)
            if agents:
                router.register_agents({
                    "rag": agents[0] if args.use_rag else None,
                    "tool": agents[1] if args.use_tool else None,
                    "memory": agents[2] if args.use_memory else None
                })
            agents.append(router)
        if args.use_reasoning:
            reasoning_agent = ReasoningAgent(model_name=args.model)
            # 设置推理技巧
            reasoning_agent.reasoning_techniques.update({
                "zero_shot": args.zero_shot,
                "few_shot": args.few_shot,
                "one_shot": args.one_shot,
                "cot": args.cot,
                "least_to_most": args.least_to_most,
                "self_consistency": args.self_consistency,
                "react": args.react,
                "reflection": args.reflection,
                "tot": args.tot
            })
            agents.append(reasoning_agent)
            
        if not agents:
            # 如果没有选择任何代理，默认使用RAG代理
            agents.append(RAGAgent(model_name=args.model))
            
        # 处理任务
        result = args.task
        for agent in agents:
            result = agent.process(args.task, result)
            
        print("\n结果:")
        print(result)
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 