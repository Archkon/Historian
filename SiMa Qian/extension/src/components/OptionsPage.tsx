declare global {
  interface Window {
    React: any;
  }
}



import { useAppState } from '../hooks/useAppState';
import { AgentSection } from './AgentSection';
import { APISettingsSection } from './APISettings';
import { ModelParametersSection } from './ModelParameters';
import { ReasoningTechniquesSection } from './ReasoningTechniques';

export function OptionsPage() {
  const { state, updateState } = useAppState();

  return window.React.createElement('div', { className: 'min-h-screen bg-gray-100 py-6 px-4 sm:px-6 lg:px-8' }, [
    window.React.createElement('div', { key: 'container', className: 'max-w-3xl mx-auto space-y-6' }, [
      window.React.createElement('div', { key: 'header', className: 'text-center' }, [
        window.React.createElement('h2', { className: 'text-3xl font-bold text-gray-900' }, '史记助手设置'),
        window.React.createElement('p', { className: 'mt-2 text-sm text-gray-600' }, '配置您的AI历史研究助手')
      ]),
      window.React.createElement('div', { key: 'sections', className: 'space-y-6' }, [
        window.React.createElement(AgentSection, {
          key: 'agent',
          agent: state.agent,
          onUpdate: (agent: any) => updateState({ agent })
        }),
        window.React.createElement(APISettingsSection, {
          key: 'api', 
          settings: state.apiSettings,
          onUpdate: (apiSettings: any) => updateState({ apiSettings })
        }),
        window.React.createElement(ModelParametersSection, {
          key: 'model',
          parameters: state.modelParameters,
          onUpdate: (modelParameters: any) => updateState({ modelParameters })
        }),
        window.React.createElement(ReasoningTechniquesSection, {
          key: 'reasoning',
          techniques: state.reasoningTechniques,
          onUpdate: (reasoningTechniques: any) => updateState({ reasoningTechniques })
        })
      ])
    ])
  ]);
} 