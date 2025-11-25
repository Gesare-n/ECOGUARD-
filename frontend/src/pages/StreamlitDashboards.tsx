// Streamlit Dashboards page for EcoGuard

import { useState } from 'react';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';

const StreamlitDashboards = () => {
  const [selectedDashboard, setSelectedDashboard] = useState<string | null>(null);
  const [showDashboard, setShowDashboard] = useState(false);

  const dashboards = [
    {
      id: 'main',
      name: 'Main Dashboard',
      description: 'The primary EcoGuard dashboard with overview of all forest monitoring systems',
      file: 'streamlit_dashboard.py',
      port: 8501
    },
    {
      id: 'institutional',
      name: 'Institutional Dashboard',
      description: 'Dashboard for institutional users with advanced management features',
      file: 'institutional_dashboard.py',
      port: 8502
    },
    {
      id: 'policy',
      name: 'Policy Dashboard',
      description: 'Dashboard for policy makers with aggregated data and insights',
      file: 'policy_dashboard.py',
      port: 8503
    },
    {
      id: 'research',
      name: 'Research Dashboard',
      description: 'Dashboard for researchers with detailed data analysis tools',
      file: 'research_dashboard.py',
      port: 8504
    },
    {
      id: 'nairobi',
      name: 'Nairobi Forest Dashboard',
      description: 'Specialized dashboard for monitoring Nairobi\'s urban forests',
      file: 'nairobi_dashboard.py',
      port: 8505
    },
    {
      id: 'enhanced',
      name: 'Enhanced Dashboard',
      description: 'Advanced dashboard with additional analytics and reporting features',
      file: 'enhanced_dashboard.py',
      port: 8506
    },
    {
      id: 'super-user',
      name: 'Super User Dashboard',
      description: 'Administrative dashboard with full system access and user management',
      file: 'super_user_dashboard.py',
      port: 8507
    }
  ];

  const handleLaunchDashboard = (dashboard: any) => {
    setSelectedDashboard(dashboard.id);
    setShowDashboard(true);
  };

  const handleBackToList = () => {
    setShowDashboard(false);
    setSelectedDashboard(null);
  };

  // If a dashboard is selected, show it in an iframe
  if (showDashboard && selectedDashboard) {
    const dashboard = dashboards.find(d => d.id === selectedDashboard);
    if (dashboard) {
      return (
        <div className="min-h-screen bg-background">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-bold text-foreground">{dashboard.name}</h1>
              <Button 
                onClick={handleBackToList}
                className="bg-primary hover:bg-primary/90"
              >
                ← Back to Dashboard List
              </Button>
            </div>
            <div className="bg-white rounded-lg border border-border shadow-sm overflow-hidden">
              <iframe 
                src={`http://localhost:${dashboard.port}`} 
                className="w-full h-screen"
                title={dashboard.name}
                onError={(e) => {
                  console.error('Failed to load dashboard:', e);
                }}
              />
            </div>
            <div className="mt-4 p-4 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                <strong>Note:</strong> If the dashboard doesn't load, please make sure you've started the Streamlit server for this dashboard. 
                You can run <code className="bg-background px-1 rounded">run_{dashboard.id}_dashboard.bat</code> or 
                <code className="bg-background px-1 rounded">run_all_dashboards.bat</code> to start all dashboards.
              </p>
            </div>
          </div>
        </div>
      );
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            EcoGuard Dashboards
          </h1>
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
            Access all EcoGuard dashboards from this unified interface
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {dashboards.map((dashboard) => (
            <Card key={dashboard.id} className="p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
              <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <span className="text-xl">📊</span>
              </div>
              <h2 className="text-xl font-bold mb-2">{dashboard.name}</h2>
              <p className="text-muted-foreground mb-4 text-sm">{dashboard.description}</p>
              <Button 
                onClick={() => handleLaunchDashboard(dashboard)}
                className="w-full bg-primary hover:bg-primary/90"
              >
                Open Dashboard
              </Button>
            </Card>
          ))}
        </div>

        <Card className="p-6 md:p-8">
          <h2 className="text-2xl font-bold mb-6 text-center">How to Access Dashboards</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                  <span className="text-primary">1</span>
                </span>
                Starting Dashboards
              </h3>
              <p className="text-muted-foreground mb-4">
                Before accessing the dashboards, you need to start the Streamlit servers:
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>Run <code className="bg-background px-1 rounded">run_all_dashboards.bat</code> to start all dashboards at once</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>Or run individual dashboard files like <code className="bg-background px-1 rounded">run_main_dashboard.bat</code></span>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center">
                <span className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center mr-3">
                  <span className="text-primary">2</span>
                </span>
                Accessing Dashboards
              </h3>
              <p className="text-muted-foreground mb-4">
                Once the servers are running:
              </p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>Click "Open Dashboard" on any dashboard card above</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>The dashboard will load within this interface</span>
                </li>
                <li className="flex items-start">
                  <span className="text-primary mr-2">•</span>
                  <span>Use the back button to return to this list</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default StreamlitDashboards;