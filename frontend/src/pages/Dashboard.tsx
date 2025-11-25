// Dashboard component for EcoGuard - shows different content based on user role

import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import ForestMap from '../components/maps/Map';

const Dashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');

  // Render content based on user role
  const renderDashboardContent = () => {
    if (!user) return null;

    switch (user.role) {
      case 'forest_ranger':
        return (
          <div className="space-y-6 md:space-y-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">12</div>
                <div className="text-xs md:text-sm text-muted-foreground">Active Sensors</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">3</div>
                <div className="text-xs md:text-sm text-muted-foreground">Alerts Today</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">87%</div>
                <div className="text-xs md:text-sm text-muted-foreground">Battery Avg</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">98%</div>
                <div className="text-xs md:text-sm text-muted-foreground">Signal Strength</div>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
              <Card className="p-4 md:p-6">
                <h2 className="text-xl md:text-2xl font-bold mb-4">Live Forest Map</h2>
                <ForestMap />
              </Card>

              <div className="space-y-6">
                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Recent Alerts</h2>
                  <div className="space-y-4">
                    {[
                      { id: 1, type: 'Chainsaw Detected', forest: 'Karura Forest', time: '2 hours ago', priority: 'High' },
                      { id: 2, type: 'Unusual Activity', forest: 'Uhuru Park', time: '5 hours ago', priority: 'Medium' },
                    ].map(alert => (
                      <div key={alert.id} className="border-b pb-4 last:border-0 last:pb-0">
                        <div className="flex justify-between">
                          <h3 className="font-medium text-sm md:text-base">{alert.type}</h3>
                          <span className={`px-2 py-1 rounded text-xs ${
                            alert.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                          }`}>
                            {alert.priority}
                          </span>
                        </div>
                        <p className="text-xs md:text-sm text-muted-foreground">{alert.forest} • {alert.time}</p>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Your Region: {user.region}</h2>
                  <p className="text-sm md:text-base text-muted-foreground mb-4">Organization: {user.organization}</p>
                  <div className="bg-muted rounded-lg p-4">
                    <h3 className="font-medium mb-2">Daily Report</h3>
                    <p className="text-sm">All sensors operational. No critical alerts in the last 24 hours.</p>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        );

      case 'regional_manager':
        return (
          <div className="space-y-6 md:space-y-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">48</div>
                <div className="text-xs md:text-sm text-muted-foreground">Active Sensors</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">12</div>
                <div className="text-xs md:text-sm text-muted-foreground">Alerts This Week</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">92%</div>
                <div className="text-xs md:text-sm text-muted-foreground">System Uptime</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">3</div>
                <div className="text-xs md:text-sm text-muted-foreground">Teams Active</div>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
              <Card className="p-4 md:p-6">
                <h2 className="text-xl md:text-2xl font-bold mb-4">Regional Overview: {user.region}</h2>
                <p className="text-sm md:text-base text-muted-foreground mb-4">Organization: {user.organization}</p>
                <div className="space-y-4">
                  {[
                    { forest: 'Karura Forest', sensors: 12, alerts: 3, status: 'Operational' },
                    { forest: 'Uhuru Park', sensors: 8, alerts: 1, status: 'Operational' },
                    { forest: 'Ngong Forest', sensors: 15, alerts: 5, status: 'Warning' },
                  ].map((region, index) => (
                    <div key={index} className="border-b pb-4 last:border-0 last:pb-0">
                      <div className="flex justify-between">
                        <h3 className="font-medium text-sm md:text-base">{region.forest}</h3>
                        <span className={`px-2 py-1 rounded text-xs ${
                          region.status === 'Operational' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {region.status}
                        </span>
                      </div>
                      <p className="text-xs md:text-sm text-muted-foreground">
                        {region.sensors} sensors • {region.alerts} alerts
                      </p>
                    </div>
                  ))}
                </div>
              </Card>

              <div className="space-y-6">
                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Live Regional Map</h2>
                  <ForestMap />
                </Card>

                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Team Performance</h2>
                  <div className="space-y-4">
                    {[
                      { team: 'Alpha Team', ranger: 'John Ranger', alerts: 5, response: '2 hours' },
                      { team: 'Beta Team', ranger: 'Mary Mwangi', alerts: 3, response: '1.5 hours' },
                    ].map((team, index) => (
                      <div key={index} className="border-b pb-4 last:border-0 last:pb-0">
                        <div className="flex justify-between">
                          <h3 className="font-medium text-sm md:text-base">{team.team}</h3>
                          <span className="text-xs md:text-sm text-muted-foreground">{team.ranger}</span>
                        </div>
                        <p className="text-xs md:text-sm text-muted-foreground">
                          {team.alerts} alerts handled • Avg. response: {team.response}
                        </p>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            </div>
          </div>
        );

      case 'super_user':
        return (
          <div className="space-y-6 md:space-y-8">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">234</div>
                <div className="text-xs md:text-sm text-muted-foreground">Total Sensors</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">42</div>
                <div className="text-xs md:text-sm text-muted-foreground">Active Alerts</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">89%</div>
                <div className="text-xs md:text-sm text-muted-foreground">Overall Uptime</div>
              </Card>
              <Card className="p-4 md:p-6 text-center">
                <div className="text-2xl md:text-3xl font-bold text-primary">18</div>
                <div className="text-xs md:text-sm text-muted-foreground">Organizations</div>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
              <Card className="p-4 md:p-6">
                <h2 className="text-xl md:text-2xl font-bold mb-4">System-Wide Overview</h2>
                <div className="space-y-4">
                  {[
                    { region: 'Nairobi', forests: 5, sensors: 48, alerts: 12 },
                    { region: 'Central Kenya', forests: 8, sensors: 76, alerts: 8 },
                    { region: 'Coast', forests: 3, sensors: 32, alerts: 5 },
                  ].map((region, index) => (
                    <div key={index} className="border-b pb-4 last:border-0 last:pb-0">
                      <h3 className="font-medium text-sm md:text-base">{region.region}</h3>
                      <p className="text-xs md:text-sm text-muted-foreground">
                        {region.forests} forests • {region.sensors} sensors • {region.alerts} alerts
                      </p>
                    </div>
                  ))}
                </div>
              </Card>

              <div className="space-y-6">
                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Live System Map</h2>
                  <ForestMap />
                </Card>

                <Card className="p-4 md:p-6">
                  <h2 className="text-xl md:text-2xl font-bold mb-4">Organization Management</h2>
                  <div className="space-y-4">
                    <Button className="w-full mb-4">Add New Organization</Button>
                    <div className="max-h-60 overflow-y-auto">
                      {[
                        { org: 'Nairobi Conservation Team', region: 'Nairobi', status: 'Active' },
                        { org: 'Central Kenya Forest Authority', region: 'Central Kenya', status: 'Active' },
                        { org: 'Coast Environmental Group', region: 'Coast', status: 'Pending' },
                      ].map((org, index) => (
                        <div key={index} className="border-b pb-3 last:border-0 last:pb-0">
                          <div className="flex justify-between">
                            <h3 className="font-medium text-sm md:text-base">{org.org}</h3>
                            <span className={`px-2 py-1 rounded text-xs ${
                              org.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                            }`}>
                              {org.status}
                            </span>
                          </div>
                          <p className="text-xs md:text-sm text-muted-foreground">{org.region}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-center py-12">
            <h2 className="text-xl md:text-2xl font-bold mb-4">Welcome to EcoGuard</h2>
            <p className="text-muted-foreground">Your role-based dashboard is loading...</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-6 md:py-8">
        <div className="mb-6 md:mb-8">
          <h1 className="text-2xl md:text-4xl font-bold mb-2">Dashboard</h1>
          <p className="text-muted-foreground text-sm md:text-base">
            Welcome back, {user?.name}. Here's what's happening in your region.
          </p>
        </div>

        <div className="mb-6 md:mb-8">
          <div className="flex space-x-1 bg-muted rounded-lg p-1 inline-flex overflow-x-auto">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-3 py-2 md:px-4 md:py-2 rounded-md text-xs md:text-sm font-medium transition-colors whitespace-nowrap ${
                activeTab === 'overview'
                  ? 'bg-background shadow'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`px-3 py-2 md:px-4 md:py-2 rounded-md text-xs md:text-sm font-medium transition-colors whitespace-nowrap ${
                activeTab === 'reports'
                  ? 'bg-background shadow'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              Reports
            </button>
            {user?.role === 'super_user' && (
              <button
                onClick={() => setActiveTab('admin')}
                className={`px-3 py-2 md:px-4 md:py-2 rounded-md text-xs md:text-sm font-medium transition-colors whitespace-nowrap ${
                  activeTab === 'admin'
                    ? 'bg-background shadow'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                Admin
              </button>
            )}
          </div>
        </div>

        {renderDashboardContent()}
      </div>
    </div>
  );
};

export default Dashboard;