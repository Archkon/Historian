declare global {
  interface Window {
    React: any;
  }
}



import { ModelParameters } from '../types';

interface ModelParametersSectionProps {
  parameters: ModelParameters;
  onUpdate: (parameters: ModelParameters) => void;
}

interface ParameterSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  onChange: (value: number) => void;
}

function ParameterSlider({ label, value, min, max, step, onChange }: ParameterSliderProps) {
  return window.React.createElement('div', { className: 'space-y-2' }, [
    window.React.createElement('div', { key: 'label', className: 'flex justify-between' }, [
      window.React.createElement('label', { className: 'block text-sm font-medium text-gray-700' }, label),
      window.React.createElement('span', { className: 'text-sm text-gray-500' }, value.toFixed(2))
    ]),
    window.React.createElement('input', {
      key: 'slider',
      type: 'range',
      min,
      max,
      step,
      value,
      onChange: (e: any) => onChange(parseFloat(e.target.value)),
      className: 'w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer'
    })
  ]);
}

export function ModelParametersSection({ parameters, onUpdate }: ModelParametersSectionProps) {
  const handleInputChange = (field: keyof ModelParameters, value: number) => {
    onUpdate({
      ...parameters,
      [field]: value
    });
  };

  const parameterConfigs: Record<keyof ModelParameters, { label: string; min: number; max: number; step: number }> = {
    temperature: { label: '温度', min: 0, max: 2, step: 0.1 },
    topP: { label: 'Top P', min: 0, max: 1, step: 0.05 },
    topK: { label: 'Top K', min: 1, max: 100, step: 1 },
    maxTokens: { label: '最大令牌数', min: 1, max: 4096, step: 1 },
    presencePenalty: { label: '存在惩罚', min: -2, max: 2, step: 0.1 },
    frequencyPenalty: { label: '频率惩罚', min: -2, max: 2, step: 0.1 }
  };

  return window.React.createElement('div', { className: 'space-y-4' }, [
    window.React.createElement('h3', { key: 'title', className: 'text-lg font-medium text-gray-900' }, '模型参数'),
    window.React.createElement('div', { key: 'parameters', className: 'space-y-6' },
      Object.entries(parameters).map(([key, value]) => {
        const config = parameterConfigs[key as keyof ModelParameters];
        return window.React.createElement(ParameterSlider, {
          key,
          label: config.label,
          value,
          min: config.min,
          max: config.max,
          step: config.step,
          onChange: (newValue: number) => handleInputChange(key as keyof ModelParameters, newValue)
        });
      })
    )
  ]);
} 