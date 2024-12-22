from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import sys
import json
import logging

# 添加Herodotus的src目录到Python路径
herodotus_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Herodotus/src'))
sys.path.append(herodotus_src)

# 导入代理模块
from agents.rag.rag_agent import RAGAgent
from agents.tools.tool_agent import ToolAgent
from agents.memory.memory_agent import MemoryAgent
from agents.router.router_agent import RouterAgent
from agents.reasoning.reasoning_agent import ReasoningAgent

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 全局变量存储工作流和自定义模型
workflows = []
custom_models = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    try:
        data = request.json
        task = data.get('task')
        settings = data.get('settings', {})
        
        if not task:
            return jsonify({"status": "error", "message": "任务不能为空"}), 400
            
        # 验证API密钥
        api_key = settings.get('api_key')
        if not api_key:
            return jsonify({"status": "error", "message": "API密钥不能为空"}), 400

        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        if settings.get('base_url'):
            os.environ["OPENAI_API_BASE"] = settings.get('base_url')
            
        # 初始化代理
        agents = []
        
        # LLM参数
        llm_params = {
            "model_name": settings.get('model', 'gpt-3.5-turbo'),
            "api_key": api_key,
            "api_base": settings.get('base_url', 'https://api.openai.com/v1'),
            "streaming": True,
            "temperature": settings.get('temperature', 0.7),
            "max_tokens": settings.get('max_tokens', 2000),
            "top_p": settings.get('top_p', 1.0),
            "presence_penalty": settings.get('presence_penalty', 0.0),
            "frequency_penalty": settings.get('frequency_penalty', 0.0)
        }
        
        # RAG Agent
        if settings.get('use_rag'):
            rag_params = {
                "model_name": llm_params["model_name"],
                "api_key": llm_params["api_key"],
                "api_base": llm_params["api_base"],
                "streaming": llm_params["streaming"],
                "use_embedding": settings.get('use_embedding', False),
                "use_database": settings.get('use_database', False),
                "use_retrieval": settings.get('use_retrieval', False),
                "use_rerank": settings.get('use_rerank', False)
            }
            agents.append(RAGAgent(**rag_params))
            
        # Tool Agent
        if settings.get('use_tool'):
            tool_params = {
                "model_name": llm_params["model_name"],
                "streaming": llm_params["streaming"]
            }
            tool_agent = ToolAgent(**tool_params)
            # 设置工具代理的特定参数
            tool_agent.use_code_tool = settings.get('use_code_tool', False)
            tool_agent.use_shell_tool = settings.get('use_shell_tool', False)
            tool_agent.use_web_tool = settings.get('use_web_tool', False)
            tool_agent.use_file_tool = settings.get('use_file_tool', False)
            agents.append(tool_agent)
            
        # Memory Agent
        if settings.get('use_memory'):
            memory_params = {
                "model_name": llm_params["model_name"]
            }
            memory_agent = MemoryAgent(**memory_params)
            # 设置记忆代理的特定参数
            memory_agent.use_conversation_memory = settings.get('use_conversation_memory', False)
            memory_agent.use_summary_memory = settings.get('use_summary_memory', False)
            memory_agent.use_vector_memory = settings.get('use_vector_memory', False)
            agents.append(memory_agent)
            
        # Router Agent
        if settings.get('use_router'):
            router_params = {
                "model_name": llm_params["model_name"]
            }
            router = RouterAgent(**router_params)
            # 设置路由代理的特定参数
            router.use_output_agent = settings.get('use_output_agent', False)
            router.use_evaluation_agent = settings.get('use_evaluation_agent', False)
            router.use_prompt_agent = settings.get('use_prompt_agent', False)
            if agents:
                router.register_agents({
                    "rag": agents[0] if settings.get('use_rag') else None,
                    "tool": agents[1] if settings.get('use_tool') else None,
                    "memory": agents[2] if settings.get('use_memory') else None
                })
            agents.append(router)
            
        # Reasoning Agent
        if settings.get('use_reasoning'):
            reasoning_params = {
                "model_name": llm_params["model_name"]
            }
            reasoning_agent = ReasoningAgent(**reasoning_params)
            # 设置推理技巧
            reasoning_agent.reasoning_techniques = {
                k: settings.get(k, False) for k in [
                    'zero_shot', 'few_shot', 'one_shot', 'cot',
                    'least_to_most', 'self_consistency', 'react',
                    'reflection', 'tot'
                ]
            }
            agents.append(reasoning_agent)
        
        if not agents:
            default_params = {
                "model_name": llm_params["model_name"],
                "api_key": llm_params["api_key"],
                "api_base": llm_params["api_base"],
                "streaming": llm_params["streaming"]
            }
            agents.append(RAGAgent(**default_params))
        
        # 处理任务
        result = task
        for agent in agents:
            # 设置LLM参数
            agent.update_config({
                "model": llm_params["model_name"],
                "temperature": llm_params["temperature"],
                "max_tokens": llm_params["max_tokens"],
                "top_p": llm_params["top_p"],
                "presence_penalty": llm_params["presence_penalty"],
                "frequency_penalty": llm_params["frequency_penalty"],
                "stream_output": llm_params["streaming"],
                "openai_api_key": llm_params["api_key"],
                "openai_api_base": llm_params["api_base"]
            })
            result = agent.process(task, result)
        
        return jsonify({
            "status": "success",
            "result": result
        })
        
    except Exception as e:
        logger.error(f"处理任务时出错: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"处理任务时出错: {str(e)}"
        }), 500

@app.route('/api/workflow', methods=['GET'])
def get_workflows():
    return jsonify({"workflows": workflows})

@app.route('/api/workflow', methods=['POST'])
def save_workflow():
    try:
        data = request.json
        workflow_name = data.get('name')
        workflow_steps = data.get('steps')
        
        if not workflow_name or not workflow_steps:
            return jsonify({"status": "error", "message": "工作流名称和步骤不能为空"}), 400
            
        # 验证工作流步骤
        for step in workflow_steps:
            if not isinstance(step, dict):
                return jsonify({"status": "error", "message": "工作流步骤格式无效"}), 400
            
            # 验证自定义模型
            if step.get('model') == 'custom':
                custom_model = step.get('custom_model')
                if not custom_model or not custom_model.get('name'):
                    return jsonify({"status": "error", "message": "自定义模型配置无效"}), 400
                
        workflows.append({
            "name": workflow_name,
            "steps": workflow_steps
        })
        
        return jsonify({"status": "success", "message": "工作流保存成功"})
        
    except Exception as e:
        logger.error(f"保存工作流时出错: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/workflow/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    try:
        if 0 <= workflow_id < len(workflows):
            del workflows[workflow_id]
            return jsonify({"status": "success", "message": "工作流删除成功"})
        return jsonify({"status": "error", "message": "工作流不存在"}), 404
    except Exception as e:
        logger.error(f"删除工作流时出错: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/workflow/<int:workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    try:
        if not 0 <= workflow_id < len(workflows):
            return jsonify({"status": "error", "message": "工作流不存在"}), 404
            
        workflow = workflows[workflow_id]
        task = request.json.get('task')
        
        if not task:
            return jsonify({"status": "error", "message": "任务不能为空"}), 400
            
        result = task
        for step in workflow['steps']:
            # 创建步骤的设置
            settings = {
                'model': step['model'],
                'temperature': step['parameters']['temperature'],
                'max_tokens': step['parameters']['max_tokens'],
                'top_p': step['parameters']['top_p'],
                'top_k': step['parameters']['top_k'],
                'presence_penalty': step['parameters']['presence_penalty'],
                'frequency_penalty': step['parameters']['frequency_penalty']
            }
            
            # 添加代理设置
            settings.update(step['agents'])
            settings.update(step['agent_components'])
            
            # 如果是推理代理，添加推理技巧
            if step['agents'].get('reasoning'):
                settings.update(step['reasoning_techniques'])
            
            # 如果是自定义模型，添加相关设置
            if step['model'] == 'custom':
                settings['custom_model_name'] = step['custom_model']['name']
                settings['base_url'] = step.get('base_url', 'https://api.openai.com/v1')
                if step.get('api_key'):
                    settings['api_key'] = step['api_key']
                if step.get('org_id'):
                    settings['org_id'] = step['org_id']
            
            # 处理这个步骤
            response = process_step(task, settings)
            if response.get('status') == 'error':
                return response
            
            result = response['result']
            
        return jsonify({
            "status": "success",
            "result": result
        })
        
    except Exception as e:
        logger.error(f"执行工作流时出错: {str(e)}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": f"执行工作流时出错: {str(e)}"
        }), 500

def process_step(task, settings):
    """处理单个工作流步骤"""
    try:
        # 验证API密钥
        api_key = settings.get('api_key')
        if not api_key:
            return {
                "status": "error",
                "message": "API密钥不能为空"
            }
            
        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        if settings.get('base_url'):
            os.environ["OPENAI_API_BASE"] = settings.get('base_url')
            
        # LLM参数
        llm_params = {
            "model_name": settings.get('model', 'gpt-3.5-turbo'),
            "api_key": api_key,
            "api_base": settings.get('base_url', 'https://api.openai.com/v1'),
            "streaming": True,
            "temperature": settings.get('temperature', 0.7),
            "max_tokens": settings.get('max_tokens', 2000),
            "top_p": settings.get('top_p', 1.0),
            "presence_penalty": settings.get('presence_penalty', 0.0),
            "frequency_penalty": settings.get('frequency_penalty', 0.0)
        }
        
        # 初始化代理
        agents = []
        
        # RAG Agent
        if settings.get('use_rag'):
            rag_params = {
                "model_name": llm_params["model_name"],
                "api_key": llm_params["api_key"],
                "api_base": llm_params["api_base"],
                "streaming": llm_params["streaming"],
                "use_embedding": settings.get('use_embedding', False),
                "use_database": settings.get('use_database', False),
                "use_retrieval": settings.get('use_retrieval', False),
                "use_rerank": settings.get('use_rerank', False)
            }
            agents.append(RAGAgent(**rag_params))
        
        # Tool Agent
        if settings.get('use_tool'):
            tool_params = {
                "model_name": llm_params["model_name"],
                "streaming": llm_params["streaming"]
            }
            tool_agent = ToolAgent(**tool_params)
            # 设置工具代理的特定参数
            tool_agent.use_code_tool = settings.get('use_code_tool', False)
            tool_agent.use_shell_tool = settings.get('use_shell_tool', False)
            tool_agent.use_web_tool = settings.get('use_web_tool', False)
            tool_agent.use_file_tool = settings.get('use_file_tool', False)
            agents.append(tool_agent)
        
        # Memory Agent
        if settings.get('use_memory'):
            memory_params = {
                "model_name": llm_params["model_name"]
            }
            memory_agent = MemoryAgent(**memory_params)
            # 设置记忆代理的特定参数
            memory_agent.use_conversation_memory = settings.get('use_conversation_memory', False)
            memory_agent.use_summary_memory = settings.get('use_summary_memory', False)
            memory_agent.use_vector_memory = settings.get('use_vector_memory', False)
            agents.append(memory_agent)
        
        # Router Agent
        if settings.get('use_router'):
            router_params = {
                "model_name": llm_params["model_name"]
            }
            router = RouterAgent(**router_params)
            # 设置路由代理的特定参数
            router.use_output_agent = settings.get('use_output_agent', False)
            router.use_evaluation_agent = settings.get('use_evaluation_agent', False)
            router.use_prompt_agent = settings.get('use_prompt_agent', False)
            if agents:
                router.register_agents({
                    "rag": agents[0] if settings.get('use_rag') else None,
                    "tool": agents[1] if settings.get('use_tool') else None,
                    "memory": agents[2] if settings.get('use_memory') else None
                })
            agents.append(router)
        
        # Reasoning Agent
        if settings.get('use_reasoning'):
            reasoning_params = {
                "model_name": llm_params["model_name"]
            }
            reasoning_agent = ReasoningAgent(**reasoning_params)
            # 设置推理技巧
            reasoning_agent.reasoning_techniques = {
                k: settings.get(k, False) for k in [
                    'zero_shot', 'few_shot', 'one_shot', 'cot',
                    'least_to_most', 'self_consistency', 'react',
                    'reflection', 'tot'
                ]
            }
            agents.append(reasoning_agent)
        
        if not agents:
            default_params = {
                "model_name": llm_params["model_name"],
                "api_key": llm_params["api_key"],
                "api_base": llm_params["api_base"],
                "streaming": llm_params["streaming"]
            }
            agents.append(RAGAgent(**default_params))
        
        # 处理任务
        result = task
        for agent in agents:
            # 设置LLM参数
            agent.update_config({
                "model": llm_params["model_name"],
                "temperature": llm_params["temperature"],
                "max_tokens": llm_params["max_tokens"],
                "top_p": llm_params["top_p"],
                "presence_penalty": llm_params["presence_penalty"],
                "frequency_penalty": llm_params["frequency_penalty"],
                "stream_output": llm_params["streaming"],
                "openai_api_key": llm_params["api_key"],
                "openai_api_base": llm_params["api_base"]
            })
            result = agent.process(task, result)
        
        return {
            "status": "success",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"处理步骤时出错: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": f"处理步骤时出错: {str(e)}"
        }

if __name__ == '__main__':
    app.run(debug=True) 