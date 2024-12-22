declare global {
  interface Window {
    React: {
      createElement: (type: any, props?: any, ...children: any[]) => any;
      useState: <T>(initialState: T | (() => T)) => [T, (newState: T | ((prevState: T) => T)) => void];
      useEffect: (effect: () => void | (() => void), deps?: any[]) => void;
      StrictMode: any;
    };
    ReactDOM: {
      createRoot: (container: Element | null) => {
        render: (element: any) => void;
      };
    };
    chrome: {
      runtime: {
        openOptionsPage: () => void;
      };
      storage: {
        local: {
          get: <T = any>(keys: string[]) => Promise<{ [key: string]: T }>;
          set: (items: { [key: string]: any }) => Promise<void>;
        };
      };
    };
    langchain: {
      OpenAI: new (config: {
        openAIApiKey: string;
        modelName: string;
        temperature: number;
        maxTokens: number;
        baseURL: string;
      }) => {
        invoke: (prompt: string) => Promise<string>;
      };
    };
  }
}

export {}; 