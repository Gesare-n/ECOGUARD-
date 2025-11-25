// Simple tabs component placeholder
// This would be replaced with a full shadcn/ui implementation when dependencies are installed

export const Tabs = ({ children, value, onValueChange, ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: 'w-full',
      ...props,
      children
    }
  };
};

export const TabsList = ({ children, className = "", ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: `inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground ${className}`,
      ...props,
      children
    }
  };
};

export const TabsTrigger = ({ children, value, className = "", ...props }: any) => {
  return {
    type: 'button',
    props: {
      className: `inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm ${className}`,
      ...props,
      children
    }
  };
};

export const TabsContent = ({ children, value, className = "", ...props }: any) => {
  return {
    type: 'div',
    props: {
      className: `mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ${className}`,
      ...props,
      children
    }
  };
};