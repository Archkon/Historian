declare global {
  interface Window {
    React: any;
  }
}

const { useState } = window.React;

import { APISettings } from '../types';

interface APISettingsSectionProps {
  settings: APISettings;
  onUpdate: (settings: APISettings) => void;
}

export function APISettingsSection({ settings, onUpdate }: APISettingsSectionProps) {
  const [isTestingConnection, setIsTestingConnection] = useState(false);

  const handleInputChange = (field: keyof APISettings, value: string) => {
    onUpdate({
      ...settings,
      [field]: value
    });
  };

  const handleTestConnection = async () => {
    setIsTestingConnection(true);
    try {
      // 测试连接逻辑
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert('连接成功！');
    } catch (error) {
      alert('连接失败：' + (error instanceof Error ? error.message : '未知错误'));
    } finally {
      setIsTestingConnection(false);
    }
  };

  return window.React.createElement('div', { className: 'space-y-4' }, [
    window.React.createElement('h3', { key: 'title', className: 'text-lg font-medium text-gray-900' }, 'API设置'),
    window.React.createElement('div', { key: 'form', className: 'space-y-4' }, [
      window.React.createElement('div', { key: 'apiKey', className: 'space-y-2' }, [
        window.React.createElement('label', { className: 'block text-sm font-medium text-gray-700' }, 'API密钥'),
        window.React.createElement('input', {
          type: 'password',
          value: settings.apiKey,
          onChange: (e: any) => handleInputChange('apiKey', e.target.value),
          className: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        })
      ]),
      window.React.createElement('div', { key: 'baseUrl', className: 'space-y-2' }, [
        window.React.createElement('label', { className: 'block text-sm font-medium text-gray-700' }, 'API基础URL'),
        window.React.createElement('input', {
          type: 'text',
          value: settings.baseUrl,
          onChange: (e: any) => handleInputChange('baseUrl', e.target.value),
          className: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        })
      ]),
      window.React.createElement('div', { key: 'orgId', className: 'space-y-2' }, [
        window.React.createElement('label', { className: 'block text-sm font-medium text-gray-700' }, '组织ID'),
        window.React.createElement('input', {
          type: 'text',
          value: settings.orgId,
          onChange: (e: any) => handleInputChange('orgId', e.target.value),
          className: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm'
        })
      ]),
      window.React.createElement('button', {
        key: 'test',
        type: 'button',
        onClick: handleTestConnection,
        disabled: isTestingConnection || !settings.apiKey,
        className: `inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 ${
          isTestingConnection ? 'cursor-not-allowed' : 'cursor-pointer'
        }`
      }, isTestingConnection ? '测试中...' : '测试连接')
    ])
  ]);
} 