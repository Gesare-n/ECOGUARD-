import { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';
import { useToast, Toaster } from './components/ui/toast';

const AppWithToast = () => {
  const { toast, toasts, dismiss } = useToast();
  
  // Make toast available globally for testing
  (window as any).toast = toast;
  
  return (
    <div className="relative">
      <App />
      <Toaster toasts={toasts} dismiss={dismiss} />
    </div>
  );
};

const rootElement = document.getElementById('root');
if (rootElement) {
  createRoot(rootElement).render(<AppWithToast />);
} else {
  console.error('Failed to find the root element');
}