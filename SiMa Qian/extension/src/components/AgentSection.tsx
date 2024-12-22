declare global {
  interface Window {
    React: any;
  }
}



import { Agent } from '../types';

interface AgentSectionProps {
  agent: Agent;
  onUpdate: (agent: Agent) => void;
}

interface AgentComponentProps {
  name: string;
  enabled: boolean;
  onToggle: () => void;
}

function AgentComponent({ name, enabled, onToggle }: AgentComponentProps) {
  return window.React.createElement('div', { className: 'flex items-center justify-between' }, [
    window.React.createElement('span', { key: 'label', className: 'text-sm text-gray-700' }, name),
    window.React.createElement('button', {
      key: 'toggle',
      type: 'button',
      onClick: onToggle,
      className: `relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
        enabled ? 'bg-primary-600' : 'bg-gray-200'
      }`
    }, [
      window.React.createElement('span', {
        className: `pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
          enabled ? 'translate-x-4' : 'translate-x-0'
        }`
      })
    ])
  ]);
}

export function AgentSection({ agent, onUpdate }: AgentSectionProps) {
  const handleToggleEnabled = () => {
    onUpdate({
      ...agent,
      enabled: !agent.enabled
    });
  };

  const handleToggleComponent = (component: keyof Agent['components']) => {
    onUpdate({
      ...agent,
      components: {
        ...agent.components,
        [component]: !agent.components[component]
      }
    });
  };

  const componentLabels: Record<keyof Agent['components'], string> = {
    rag: 'RAG代理',
    tool: '工具代理',
    memory: '记忆代理',
    router: '路由代理',
    reasoning: '推理代理'
  };

  return window.React.createElement('div', { className: 'space-y-4' }, [
    window.React.createElement('div', { key: 'header', className: 'flex items-center justify-between' }, [
      window.React.createElement('h3', { className: 'text-lg font-medium text-gray-900' }, '代理设置'),
      window.React.createElement('button', {
        type: 'button',
        onClick: handleToggleEnabled,
        className: `relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
          agent.enabled ? 'bg-primary-600' : 'bg-gray-200'
        }`
      }, [
        window.React.createElement('span', {
          className: `pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
            agent.enabled ? 'translate-x-5' : 'translate-x-0'
          }`
        })
      ])
    ]),
    window.React.createElement('div', { key: 'components', className: 'space-y-2' },
      Object.entries(agent.components).map(([key, value]) =>
        window.React.createElement(AgentComponent, {
          key,
          name: componentLabels[key as keyof Agent['components']],
          enabled: value,
          onToggle: () => handleToggleComponent(key as keyof Agent['components'])
        })
      )
    )
  ]);
} 