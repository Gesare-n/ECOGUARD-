// Simple navigation link component placeholder
// This would be replaced with a full implementation when dependencies are installed

export const NavLink = ({ children, to, className, activeClassName, ...props }: any) => {
  return {
    type: 'a',
    props: {
      href: to,
      className: className || '',
      ...props,
      children
    }
  };
};