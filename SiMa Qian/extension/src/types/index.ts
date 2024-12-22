// Agent类型
export interface Agent {
  enabled: boolean;
  components: {
    rag: boolean;
    tool: boolean;
    memory: boolean;
    router: boolean;
    reasoning: boolean;
  };
}

// 推理技巧类型
export interface ReasoningTechnique {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
}

// 模型参数类型
export interface ModelParameters {
  temperature: number;
  topP: number;
  topK: number;
  maxTokens: number;
  presencePenalty: number;
  frequencyPenalty: number;
}

// API设置类型
export interface APISettings {
  baseUrl: string;
  apiKey: string;
  orgId: string;
}

// 工作流步骤类型
export interface WorkflowStep {
  id: string;
  name: string;
  description: string;
  agents: string[];
  techniques: string[];
}

// 全局状态类型
export interface AppState {
  agent: Agent;
  apiSettings: APISettings;
  modelParameters: ModelParameters;
  reasoningTechniques: ReasoningTechnique[];
  workflow: WorkflowStep[];
  language: string;
  theme: string;
} 