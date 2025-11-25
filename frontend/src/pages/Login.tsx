// Login page component for EcoGuard frontend

import { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { useToast } from '../components/ui/toast';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error, clearError } = useAuth();
  const { toast } = useToast();

  // Clear error when component mounts
  useEffect(() => {
    clearError();
  }, [clearError]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username || !password) {
      toast({
        title: "Error",
        description: "Please enter both username and password",
        variant: "destructive"
      });
      return;
    }

    const success = await login(username, password);
    
    if (success) {
      toast({
        title: "Success",
        description: "Logged in successfully",
        variant: "success"
      });
      // Redirect to dashboard (in a real app, this would be handled by routing)
      window.location.href = '/';
    } else {
      toast({
        title: "Login Failed",
        description: "Invalid username or password",
        variant: "destructive"
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary flex items-center justify-center p-4">
      <Card className="w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🌳</span>
          </div>
          <h1 className="text-3xl font-bold">EcoGuard</h1>
          <p className="text-muted-foreground mt-2">Forest Protection System</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-2">
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
              placeholder="Enter your username"
              disabled={loading}
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
              placeholder="Enter your password"
              disabled={loading}
            />
          </div>
          
          <Button 
            type="submit" 
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
            disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                Logging in...
              </span>
            ) : (
              "Login"
            )}
          </Button>
        </form>
        
        <div className="mt-6 p-4 bg-muted rounded-lg">
          <h3 className="font-medium text-sm mb-2">Demo Credentials:</h3>
          <ul className="text-xs text-muted-foreground space-y-1">
            <li>Forest Ranger: username <code className="bg-background px-1 rounded">ranger1</code>, password <code className="bg-background px-1 rounded">password</code></li>
          </ul>
        </div>
      </Card>
    </div>
  );
};

export default LoginPage;