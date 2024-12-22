declare global {
  interface Window {
    React: any;
  }
}

const { useState } = window.React;

import { WorkflowStep } from '../types';

interface WorkflowSectionProps {
  steps: WorkflowStep[];
  onUpdate: (steps: WorkflowStep[]) => void;
}

export function WorkflowSection({ steps, onUpdate }: WorkflowSectionProps) {
  const [newStep, setNewStep] = useState({
    name: '',
    description: '',
    agents: [],
    techniques: []
  });

  const handleAddStep = () => {
    if (!newStep.name) return;
    const step: WorkflowStep = {
      id: Date.now().toString(),
      name: newStep.name,
      description: newStep.description || '',
      agents: newStep.agents || [],
      techniques: newStep.techniques || []
    };

    onUpdate([...steps, step]);
    setNewStep({ name: '', description: '', agents: [], techniques: [] });
  };

  const handleRemoveStep = (id: string) => {
    onUpdate(steps.filter(step => step.id !== id));
  };

  const handleMoveStep = (fromIndex: number, toIndex: number) => {
    const newSteps = [...steps];
    const [movedStep] = newSteps.splice(fromIndex, 1);
    newSteps.splice(toIndex, 0, movedStep);
    onUpdate(newSteps);
  };

  return window.React.createElement('div', { className: 'space-y-4' }, [
    window.React.createElement('h3', { key: 'title', className: 'text-lg font-medium text-gray-900' }, '工作流'),
    window.React.createElement('div', { key: 'form', className: 'space-y-4' }, [
      window.React.createElement('div', { key: 'input', className: 'space-y-2' }, [
        window.React.createElement('input', {
          type: 'text',
          value: newStep.name,
          onChange: (e: any) => setNewStep({ ...newStep, name: e.target.value }),
          placeholder: '步骤名称',
          className: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        }),
        window.React.createElement('textarea', {
          value: newStep.description,
          onChange: (e: any) => setNewStep({ ...newStep, description: e.target.value }),
          placeholder: '步骤描述',
          className: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        }),
        window.React.createElement('button', {
          type: 'button',
          onClick: handleAddStep,
          disabled: !newStep.name,
          className: 'mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50'
        }, '添加步骤')
      ]),
      window.React.createElement('div', { key: 'steps', className: 'space-y-2' },
        steps.map((step, index) =>
          window.React.createElement('div', { key: step.id, className: 'flex items-center justify-between p-4 bg-white rounded-lg shadow' }, [
            window.React.createElement('div', { key: 'info', className: 'space-y-1' }, [
              window.React.createElement('h4', { className: 'font-medium text-gray-900' }, step.name),
              window.React.createElement('p', { className: 'text-sm text-gray-500' }, step.description)
            ]),
            window.React.createElement('div', { key: 'actions', className: 'flex space-x-2' }, [
              index > 0 && window.React.createElement('button', {
                type: 'button',
                onClick: () => handleMoveStep(index, index - 1),
                className: 'text-gray-400 hover:text-gray-500'
              }, '↑'),
              index < steps.length - 1 && window.React.createElement('button', {
                type: 'button',
                onClick: () => handleMoveStep(index, index + 1),
                className: 'text-gray-400 hover:text-gray-500'
              }, '↓'),
              window.React.createElement('button', {
                type: 'button',
                onClick: () => handleRemoveStep(step.id),
                className: 'text-red-400 hover:text-red-500'
              }, '×')
            ])
          ])
        )
      )
    ])
  ]);
} 