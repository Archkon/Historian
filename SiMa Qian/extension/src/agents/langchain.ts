declare global {
  interface Window {
    langchain: any;
  }
}

interface LangChainServiceConfig {
  apiKey: string;
  baseUrl: string;
  modelName: string;
  temperature: number;
  maxTokens: number;
}

export class LangChainService {
  private chain: any;

  constructor(config: LangChainServiceConfig) {
    const { OpenAI } = window.langchain;
    
    const model = new OpenAI({
      openAIApiKey: config.apiKey,
      modelName: config.modelName,
      temperature: config.temperature,
      maxTokens: config.maxTokens,
      baseURL: config.baseUrl,
    });

    this.chain = model;
  }

  async analyze(text: string): Promise<string> {
    const prompt = `分析以下历史文本的背景、人物和历史意义：\n\n${text}`;
    const response = await this.chain.invoke(prompt);
    return response;
  }

  async translate(text: string): Promise<string> {
    const prompt = `将以下古文翻译成现代中文：\n\n${text}`;
    const response = await this.chain.invoke(prompt);
    return response;
  }

  async summarize(text: string): Promise<string> {
    const prompt = `总结以下历史文本的主要内容：\n\n${text}`;
    const response = await this.chain.invoke(prompt);
    return response;
  }

  async verify(text: string): Promise<string> {
    const prompt = `考证以下历史文本的真实性和可靠性：\n\n${text}`;
    const response = await this.chain.invoke(prompt);
    return response;
  }
} 