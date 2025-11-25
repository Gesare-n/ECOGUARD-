import { useState, useEffect } from 'react';

// Simple toast component placeholder
// This would be replaced with a full implementation when dependencies are installed

type Toast = {
  id: string;
  title: string;
  description?: string;
  variant?: 'default' | 'destructive' | 'success';
};

export const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);
  
  const toast = ({ title, description, variant = 'default' }: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newToast = { id, title, description, variant };
    
    setToasts(prev => [...prev, newToast]);
    
    // Auto remove toast after 5 seconds
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 5000);
  };
  
  const dismiss = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };
  
  return { toast, toasts, dismiss };
};

export const Toaster = ({ toasts, dismiss }: { toasts: Toast[], dismiss: (id: string) => void }) => {
  if (toasts.length === 0) return null;
  
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map(({ id, title, description, variant }) => (
        <div 
          key={id}
          className={`max-w-sm w-full rounded-lg border p-4 shadow-lg transition-all duration-300 ${
            variant === 'destructive' 
              ? 'bg-destructive text-destructive-foreground border-destructive' 
              : variant === 'success'
              ? 'bg-success text-success-foreground border-success'
              : 'bg-background text-foreground border-border'
          }`}
        >
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-medium">{title}</h4>
              {description && <p className="text-sm opacity-90 mt-1">{description}</p>}
            </div>
            <button 
              onClick={() => dismiss(id)}
              className="ml-4 text-muted-foreground hover:text-foreground"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};