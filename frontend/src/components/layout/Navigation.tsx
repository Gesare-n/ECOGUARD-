import { User } from '../../types/user';
import { useState } from 'react';

const Navigation = ({ currentPage, setCurrentPage, user, onLogout }: 
  { 
    currentPage: string; 
    setCurrentPage: (page: string) => void; 
    user: User | null; 
    onLogout: () => void; 
  }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="bg-background border-b border-border sticky top-0 z-50 backdrop-blur-sm bg-background/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <a 
              href="#" 
              className="flex items-center space-x-2 group"
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage('home');
                closeMenu();
              }}
            >
              <div className="w-10 h-10 rounded-lg bg-green-600 flex items-center justify-center group-hover:scale-105 transition-transform">
                <span className="text-lg text-white">🐦</span>
              </div>
              <span className="text-xl font-bold text-foreground group-hover:text-green-600 transition-colors">EcoGuard</span>
            </a>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <div className="flex space-x-1">
              <button
                onClick={() => {
                  setCurrentPage('home');
                  closeMenu();
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentPage === 'home'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                Home
              </button>
              <button
                onClick={() => {
                  setCurrentPage('about');
                  closeMenu();
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentPage === 'about'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                About
              </button>
              <button
                onClick={() => {
                  setCurrentPage('analytics');
                  closeMenu();
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentPage === 'analytics'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                Analytics
              </button>
              <button
                onClick={() => {
                  setCurrentPage('research');
                  closeMenu();
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentPage === 'research'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                Research
              </button>
              <button
                onClick={() => {
                  setCurrentPage('contact');
                  closeMenu();
                }}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentPage === 'contact'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                Contact
              </button>
              {user && (
                <>
                  <button
                    onClick={() => {
                      setCurrentPage('dashboard');
                      closeMenu();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentPage === 'dashboard'
                        ? 'bg-primary text-primary-foreground'
                        : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                    }`}
                  >
                    Dashboard
                  </button>
                  <button
                    onClick={() => {
                      setCurrentPage('streamlit');
                      closeMenu();
                    }}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentPage === 'streamlit'
                        ? 'bg-primary text-primary-foreground'
                        : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                    }`}
                  >
                    Legacy Dashboards
                  </button>
                </>
              )}
            </div>
            <div className="flex items-center space-x-4">
              {user ? (
                <div className="flex items-center space-x-3">
                  <div className="flex flex-col items-end">
                    <span className="text-sm font-medium">{user.name}</span>
                    <span className="text-xs text-muted-foreground capitalize">{user.role.replace('_', ' ')}</span>
                    <span className="text-xs text-muted-foreground">{user.organization}</span>
                  </div>
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center cursor-pointer hover:bg-primary/20 transition-colors">
                    <span className="text-sm">👤</span>
                  </div>
                  <button 
                    onClick={() => {
                      onLogout();
                      closeMenu();
                    }}
                    className="px-4 py-2 rounded-lg text-sm font-medium bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => {
                      setCurrentPage('signup');
                      closeMenu();
                    }}
                    className="px-4 py-2 rounded-lg text-sm font-medium text-foreground hover:bg-accent"
                  >
                    Register
                  </button>
                  <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center cursor-pointer hover:bg-primary/20 transition-colors">
                    <span className="text-sm">👤</span>
                  </div>
                </div>
              )}
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="flex md:hidden items-center">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-foreground hover:bg-accent focus:outline-none"
            >
              <span className="sr-only">Open main menu</span>
              {isMenuOpen ? (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <button
              onClick={() => {
                setCurrentPage('home');
                closeMenu();
              }}
              className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                currentPage === 'home'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              Home
            </button>
            <button
              onClick={() => {
                setCurrentPage('about');
                closeMenu();
              }}
              className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                currentPage === 'about'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              About
            </button>
            <button
              onClick={() => {
                setCurrentPage('analytics');
                closeMenu();
              }}
              className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                currentPage === 'analytics'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              Analytics
            </button>
            <button
              onClick={() => {
                setCurrentPage('research');
                closeMenu();
              }}
              className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                currentPage === 'research'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              Research
            </button>
            <button
              onClick={() => {
                setCurrentPage('contact');
                closeMenu();
              }}
              className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                currentPage === 'contact'
                  ? 'bg-primary text-primary-foreground'
                  : 'text-foreground hover:bg-accent hover:text-accent-foreground'
              }`}
            >
              Contact
            </button>
            {user && (
              <button
                onClick={() => {
                  setCurrentPage('streamlit');
                  closeMenu();
                }}
                className={`block px-3 py-2 rounded-md text-base font-medium w-full text-left ${
                  currentPage === 'streamlit'
                    ? 'bg-primary text-primary-foreground'
                    : 'text-foreground hover:bg-accent hover:text-accent-foreground'
                }`}
              >
                Legacy Dashboards
              </button>
            )}
            
            {user ? (
              <div className="pt-4 pb-3 border-t border-border">
                <div className="flex items-center px-3">
                  <div className="flex-shrink-0">
                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                      <span className="text-sm">👤</span>
                    </div>
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium">{user.name}</div>
                    <div className="text-sm text-muted-foreground capitalize">{user.role.replace('_', ' ')}</div>
                    <div className="text-sm text-muted-foreground">{user.organization}</div>
                  </div>
                </div>
                <div className="mt-3 px-2 space-y-1">
                  <button
                    onClick={() => {
                      setCurrentPage('dashboard');
                      closeMenu();
                    }}
                    className="block px-3 py-2 rounded-md text-base font-medium text-foreground hover:bg-accent w-full text-left"
                  >
                    Dashboard
                  </button>
                  <button
                    onClick={() => {
                      onLogout();
                      closeMenu();
                    }}
                    className="block px-3 py-2 rounded-md text-base font-medium text-foreground hover:bg-accent w-full text-left"
                  >
                    Logout
                  </button>
                </div>
              </div>
            ) : (
              <div className="pt-4 pb-3 border-t border-border">
                <div className="mt-3 px-2 space-y-1">
                  <button
                    onClick={() => {
                      setCurrentPage('signup');
                      closeMenu();
                    }}
                    className="block px-3 py-2 rounded-md text-base font-medium text-foreground hover:bg-accent w-full text-left"
                  >
                    Register
                  </button>
                  <button
                    onClick={() => {
                      setCurrentPage('login');
                      closeMenu();
                    }}
                    className="block px-3 py-2 rounded-md text-base font-medium text-foreground hover:bg-accent w-full text-left"
                  >
                    Login
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navigation;