declare global {
  interface Window {
    React: any;
  }
}



import { ReasoningTechnique } from '../types';

interface ReasoningTechniquesSectionProps {
  techniques: ReasoningTechnique[];
  onUpdate: (techniques: ReasoningTechnique[]) => void;
}

export function ReasoningTechniquesSection({ techniques, onUpdate }: ReasoningTechniquesSectionProps) {
  const handleToggleTechnique = (index: number) => {
    const updatedTechniques = techniques.map((technique, i) =>
      i === index ? { ...technique, enabled: !technique.enabled } : technique
    );
    onUpdate(updatedTechniques);
  };

  return window.React.createElement('div', { className: 'space-y-4' }, [
    window.React.createElement('h3', { key: 'title', className: 'text-lg font-medium text-gray-900' }, '推理技巧'),
    window.React.createElement('div', { key: 'techniques', className: 'space-y-2' }, 
      techniques.map((technique, index) =>
        window.React.createElement('div', { key: index, className: 'flex items-center justify-between' }, [
          window.React.createElement('div', { key: 'info', className: 'space-y-1' }, [
            window.React.createElement('span', { className: 'text-sm font-medium text-gray-900' }, technique.name),
            window.React.createElement('p', { className: 'text-xs text-gray-500' }, technique.description)
          ]),
          window.React.createElement('button', {
            key: 'toggle',
            type: 'button',
            onClick: () => handleToggleTechnique(index),
            className: `relative inline-flex h-5 w-9 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 ${
              technique.enabled ? 'bg-primary-600' : 'bg-gray-200'
            }`
          }, [
            window.React.createElement('span', {
              className: `pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                technique.enabled ? 'translate-x-4' : 'translate-x-0'
              }`
            })
          ])
        ])
      )
    )
  ]);
} 