declare global {
  interface Window {
    React: any;
    ReactDOM: any;
  }
}

import { OptionsPage } from './components/OptionsPage';
import './index.css';

const root = window.ReactDOM.createRoot(document.getElementById('root')!);
root.render(
  window.React.createElement(window.React.StrictMode, null,
    window.React.createElement(OptionsPage)
  )
); 