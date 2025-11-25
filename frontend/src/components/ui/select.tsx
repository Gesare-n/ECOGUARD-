// Simple select component placeholder
// This would be replaced with a full shadcn/ui implementation when dependencies are installed

export const Select = ({ children, value, onValueChange, ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: 'relative',
      ...props,
      children
    }
  };
};

export const SelectTrigger = ({ children, className = "", ...props }: any) => {
  return {
    type: 'button',
    props: {
      className: `flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`,
      ...props,
      children: [
        children,
        { type: 'span', props: { className: 'ml-2', children: '▼' } }
      ]
    }
  };
};

export const SelectValue = ({ placeholder }: any) => {
  return {
    type: 'span',
    props: {
      className: 'text-muted-foreground',
      children: placeholder
    }
  };
};

export const SelectContent = ({ children, className = "", ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: `absolute z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 ${className}`,
      ...props,
      children
    }
  };
};

export const SelectItem = ({ children, value, className = "", ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: `relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 ${className}`,
      ...props,
      children: [
        { type: 'span', props: { className: 'absolute left-2 flex h-3.5 w-3.5 items-center justify-center', children: '●' } },
        children
      ]
    }
  };
};