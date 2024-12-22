declare global {
  interface Window {
    React: any;
    chrome: any;
  }
}

const { useState, useEffect } = window.React;

import { AppState } from '../types';

const defaultState: AppState = {
  agent: {
    enabled: false,
    components: {
      rag: false,
      tool: false,
      memory: false,
      router: false,
      reasoning: false
    }
  },
  apiSettings: {
    baseUrl: 'https://api.openai.com/v1',
    apiKey: '',
    orgId: ''
  },
  modelParameters: {
    temperature: 0.7,
    topP: 1,
    topK: 50,
    maxTokens: 2048,
    presencePenalty: 0,
    frequencyPenalty: 0
  },
  reasoningTechniques: [
    { id: 'zeroShot', name: '零样本推理', description: '无需示例，直接进行推理', enabled: true },
    { id: 'fewShot', name: '少样本推理', description: '基于少量示例进行推理', enabled: false },
    { id: 'oneShot', name: '单样本推理', description: '基于单个示例进行推理', enabled: false },
    { id: 'cot', name: '思维链推理', description: '通过步骤分解展示推理过程', enabled: true },
    { id: 'leastToMost', name: '由简至繁推理', description: '将复杂问题分解为简单子问题', enabled: false },
    { id: 'selfConsistency', name: '自洽性推理', description: '生成多个推理路径并比较', enabled: false },
    { id: 'react', name: '反思行动推理', description: '结合推理和行动的迭代过程', enabled: false },
    { id: 'reflection', name: '自我反思推理', description: '对推理过程进行自我反思', enabled: false },
    { id: 'tot', name: '思维树推理', description: '探索多个推理分支形成决策树', enabled: false }
  ],
  workflow: [],
  language: '中文',
  theme: 'light'
};
export function useAppState() {
  const [state, setState] = useState(defaultState);

  useEffect(() => {
    // 从Chrome存储中加载状态
    window.chrome.storage.local.get(['appState'], (result: {appState?: AppState}) => {
      if (result.appState) {
        setState(result.appState);
      }
    });
  }, []);

  const updateState = (updates: Partial<AppState>) => {
    const newState = { ...state, ...updates };
    setState(newState);
    // 保存到Chrome存储
    window.chrome.storage.local.set({ appState: newState });
  };

  return { state, updateState };
} 