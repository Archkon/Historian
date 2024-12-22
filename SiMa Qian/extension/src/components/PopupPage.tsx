declare global {
  interface Window {
    React: any;
    chrome: any;
    langchain: any;
  }
}

const { useState, useEffect } = window.React;

import { LangChainService } from '../agents/langchain';
import { useAppState } from '../hooks/useAppState';

export function PopupPage() {
  const { state } = useAppState();
  const [text, setText] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [langchain, setLangchain] = useState(null as LangChainService | null);

  useEffect(() => {
    const initLangChain = () => {
      if (window.langchain) {
        const service = new LangChainService({
          apiKey: state.apiSettings.apiKey,
          baseUrl: state.apiSettings.baseUrl,
          modelName: 'gpt-4',
          temperature: state.modelParameters.temperature,
          maxTokens: state.modelParameters.maxTokens,
        });
        setLangchain(service);
      }
    };

    if (document.readyState === 'complete') {
      initLangChain();
    } else {
      window.addEventListener('load', initLangChain);
      return () => window.removeEventListener('load', initLangChain);
    }
  }, [state.apiSettings, state.modelParameters]);

  const handleAction = async (action: 'analyze' | 'translate' | 'summarize' | 'verify') => {
    if (!text || !langchain) return;
    setLoading(true);
    try {
      let result = '';
      switch (action) {
        case 'analyze':
          result = await langchain.analyze(text);
          break;
        case 'translate':
          result = await langchain.translate(text);
          break;
        case 'summarize':
          result = await langchain.summarize(text);
          break;
        case 'verify':
          result = await langchain.verify(text);
          break;
      }
      setResult(result);
    } catch (error) {
      setResult(`${action}错误: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      setLoading(false);
    }
  };

  const renderButton = (action: 'analyze' | 'translate' | 'summarize' | 'verify', label: string) => {
    return window.React.createElement('button', {
      key: action,
      onClick: () => handleAction(action),
      disabled: loading || !text,
      className: 'px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50'
    }, label);
  };

  if (!langchain) {
    return window.React.createElement('div', { className: 'w-[400px] p-4 bg-white' },
      window.React.createElement('div', { className: 'flex items-center justify-center h-32' },
        window.React.createElement('div', { className: 'text-gray-600' }, '正在加载LangChain...')
      )
    );
  }

  return window.React.createElement('div', { className: 'w-[400px] p-4 bg-white' }, [
    window.React.createElement('div', { key: 'header', className: 'flex items-center justify-between mb-4' }, [
      window.React.createElement('h1', { key: 'title', className: 'text-xl font-bold text-gray-900' }, '史记助手'),
      window.React.createElement('button', {
        key: 'settings',
        onClick: () => window.chrome.runtime.openOptionsPage(),
        className: 'text-sm text-gray-600 hover:text-gray-900'
      }, '设置')
    ]),
    window.React.createElement('textarea', {
      key: 'input',
      value: text,
      onChange: (e: any) => setText(e.target.value),
      placeholder: '请输入历史文本...',
      className: 'w-full h-32 p-2 mb-4 border rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-primary-500'
    }),
    window.React.createElement('div', { key: 'buttons', className: 'grid grid-cols-2 gap-2 mb-4' }, [
      renderButton('analyze', '分析'),
      renderButton('translate', '翻译'),
      renderButton('summarize', '摘要'),
      renderButton('verify', '考证')
    ]),
    loading ? window.React.createElement('div', { key: 'loading', className: 'flex items-center justify-center p-4' },
      window.React.createElement('div', { className: 'animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600' })
    ) : result ? window.React.createElement('div', { key: 'result', className: 'p-4 bg-gray-50 rounded-md' },
      window.React.createElement('pre', { className: 'whitespace-pre-wrap text-sm' }, result)
    ) : null
  ]);
} 