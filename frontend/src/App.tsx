import { useState, useEffect } from 'react';
import Navigation from './components/layout/Navigation';
import LoginPage from './pages/Login';
import Dashboard from './pages/Dashboard';
import OrganizationSignup from './pages/OrganizationSignup';
import HomePage from './components/layout/HomePage';
import StreamlitDashboards from './pages/StreamlitDashboards';
import { useAuth } from './hooks/useAuth';
import { Card } from './components/ui/card';
import { Button } from './components/ui/button';

type Page = 'home' | 'about' | 'contact' | 'analytics' | 'research' | 'dashboard' | 'signup' | 'streamlit';

function App() {
  const { isAuthenticated, user, logout, checkAuthStatus, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  // Check authentication status when app loads
  useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  const isCurrentPage = (page: Page) => {
    return currentPage === page;
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, this would send the form data to a server
    console.log('Form submitted:', formData);
    
    // Show success toast
    if (typeof (window as any).toast === 'function') {
      (window as any).toast({
        title: "Message Sent!",
        description: "We'll get back to you within 24 hours.",
        variant: "success"
      });
    }
    
    // Reset form
    setFormData({ name: '', email: '', message: '' });
  };

  const handleLogout = async () => {
    await logout();
    setCurrentPage('home');
    if (typeof (window as any).toast === 'function') {
      (window as any).toast({
        title: "Logged Out",
        description: "You have been successfully logged out.",
        variant: "success"
      });
    }
  };

  // Wrapper function to handle type conversion
  const handleSetCurrentPage = (page: string) => {
    // Type guard to ensure page is a valid Page type
    if (['home', 'about', 'contact', 'analytics', 'research', 'dashboard', 'signup', 'streamlit'].includes(page)) {
      setCurrentPage(page as Page);
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage setCurrentPage={handleSetCurrentPage} />;
        
      case 'signup':
        return <OrganizationSignup />;
        
      case 'dashboard':
        return <Dashboard />;
        
      case 'streamlit':
        return <StreamlitDashboards />;
        
      case 'about':
        return (
          <div className="min-h-screen bg-white">
            <div className="container mx-auto px-4 py-16 md:py-20">
              <div className="max-w-4xl mx-auto">
                {/* Hero Section */}
                <div className="text-center mb-16">
                  <div className="text-8xl mb-6">🐦</div>
                  <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">About EcoGuard</h1>
                  <p className="text-xl text-gray-700 max-w-2xl mx-auto">
                    The Digital Hummingbird - Doing the best we can to protect Kenya's forests
                  </p>
                </div>

                {/* The Hummingbird Story */}
                <section className="mb-16 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-8 md:p-12">
                  <h2 className="text-3xl md:text-4xl font-bold mb-6 text-gray-900">The Hummingbird Story</h2>
                  <p className="text-lg text-gray-700 mb-4 leading-relaxed">
                    Our positive change journey starts with a hummingbird. This story, as told by the late 
                    <strong className="font-semibold"> Prof. Wangari Maathai</strong>, Kenyan activist and the first African woman 
                    to win the Nobel Peace Prize, reminds us that even in the face of immense adversity, we can still act.
                  </p>
                  <div className="bg-white rounded-lg p-6 md:p-8 my-6 border-l-4 border-green-600">
                    <p className="text-lg text-gray-800 italic mb-4">
                      "A huge forest was being consumed by a fire, and all the animals felt powerless and overwhelmed 
                      as they watched the destruction unfold before them. All, except for one little hummingbird.
                    </p>
                    <p className="text-lg text-gray-800 italic mb-4">
                      Determined to do something about the fire, the hummingbird flew to the nearest stream and picked up 
                      a single drop of water in its tiny beak. It flew to the fire and dropped the water onto the flames. 
                      The hummingbird continued, flying up and down to the stream to gather more water, dropping it onto 
                      the fire as fast as it could.
                    </p>
                    <p className="text-lg text-gray-800 italic mb-4">
                      Despite the presence of larger animals like the elephant, who could bring more water with its big trunk, 
                      they all stood by helplessly, questioning the hummingbird's efforts. The other animals said things like:
                    </p>
                    <ul className="list-disc list-inside text-lg text-gray-800 italic mb-4 space-y-2 ml-4">
                      <li>"What do you think you can do?"</li>
                      <li>"You are too little."</li>
                      <li>"This fire is too big."</li>
                      <li>"Your wings are too small."</li>
                      <li>"Your beak can only carry a tiny drop of water. That will not make an impact."</li>
                    </ul>
                    <p className="text-lg text-gray-800 italic mb-4">
                      Paying no attention to the discouragement, the hummingbird remained resolute and responded, 
                      <strong className="font-semibold"> "I may be small and insignificant, but I will always do the best I can."</strong> 
                      The hummingbird persisted with its efforts, undeterred by the enormity of the task and the naysayers."
                    </p>
                  </div>
                  <p className="text-lg text-gray-700 leading-relaxed">
                    Prof. Maathai's story serves as a reminder that trying to make a difference and creating positive change 
                    takes courage, a sense of responsibility and persistence. Because, in the end, who would you rather be? 
                    The person who tried, or the one who stood by and did nothing?
                  </p>
                </section>

                {/* Our Mission */}
                <section className="mb-16">
                  <h2 className="text-3xl md:text-4xl font-bold mb-6 text-gray-900">Our Mission</h2>
                  <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                    EcoGuard is a revolutionary forest protection system that uses AI-powered acoustic sensors to detect 
                    illegal logging, wildfires, and other threats in Kenya's protected forests. Like the hummingbird, 
                    our sensors may be small, but they work tirelessly to do the best they can to protect our forests.
                  </p>
                  <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                    Inspired by Wangari Maathai's legacy and the Green Belt Movement, we're committed to preserving 
                    Kenya's natural heritage for future generations through innovative conservation technology.
                  </p>
                </section>

                {/* Our Technology */}
                <section className="mb-16">
                  <h2 className="text-3xl md:text-4xl font-bold mb-6 text-gray-900">Our Technology</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <Card className="p-6 border-gray-200">
                      <h3 className="text-xl font-bold mb-3">Digital Hummingbird Sensors</h3>
                      <p className="text-gray-600">
                        Raspberry Pi-based sensors in bird-shaped enclosures, powered by solar panels and equipped with 
                        USB microphones for acoustic detection and Pi cameras for visual monitoring.
                      </p>
                    </Card>
                    <Card className="p-6 border-gray-200">
                      <h3 className="text-xl font-bold mb-3">AI-Powered Detection</h3>
                      <p className="text-gray-600">
                        TensorFlow Lite models detect chainsaw sounds with {'>'}90% accuracy, running on-device for 
                        real-time threat identification.
                      </p>
                    </Card>
                    <Card className="p-6 border-gray-200">
                      <h3 className="text-xl font-bold mb-3">LoRa Communication</h3>
                      <p className="text-gray-600">
                        Long-range wireless mesh network (up to 20km) for reliable data transmission, with GSM backup 
                        for critical SMS alerts.
                      </p>
                    </Card>
                    <Card className="p-6 border-gray-200">
                      <h3 className="text-xl font-bold mb-3">Real-Time Dashboards</h3>
                      <p className="text-gray-600">
                        Interactive web dashboards for rangers, managers, and researchers with live sensor data, 
                        threat visualization, and analytics.
                      </p>
                    </Card>
                  </div>
                </section>

                {/* Impact */}
                <section className="mb-16 bg-green-600 text-white rounded-2xl p-8 md:p-12">
                  <h2 className="text-3xl md:text-4xl font-bold mb-6">Our Impact</h2>
                  <p className="text-lg mb-6 leading-relaxed">
                    Since deployment, EcoGuard has helped protect 12+ forests across Kenya, detecting 287 threats 
                    and monitoring over 3,500 hectares. Our system has contributed to Kenya's climate goals through 
                    verified carbon credit generation, saving over 12,400 tons of CO₂.
                  </p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8">
                    <div className="text-center">
                      <div className="text-3xl md:text-4xl font-bold mb-2">12+</div>
                      <div className="text-sm md:text-base">Forests</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl md:text-4xl font-bold mb-2">287</div>
                      <div className="text-sm md:text-base">Threats Detected</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl md:text-4xl font-bold mb-2">3,500+</div>
                      <div className="text-sm md:text-base">Hectares</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl md:text-4xl font-bold mb-2">12.4K</div>
                      <div className="text-sm md:text-base">Tons CO₂</div>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </div>
        );
      case 'contact':
        return (
          <div className="min-h-screen bg-white">
            <div className="container mx-auto px-4 py-16 md:py-20">
              <div className="max-w-6xl mx-auto">
                <div className="text-center mb-16">
                  <div className="text-6xl mb-4">🐦</div>
                  <h1 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">Contact Us</h1>
                  <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                    Get in touch with the EcoGuard team. We're here to help protect Kenya's forests.
                  </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                  <div>
                    <h2 className="text-3xl font-bold mb-8 text-gray-900">Get in Touch</h2>
                    <div className="space-y-8">
                      <div className="flex items-start">
                        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mr-6 flex-shrink-0">
                          <span className="text-3xl">📧</span>
                        </div>
                        <div>
                          <h3 className="text-xl font-bold mb-2 text-gray-900">Email</h3>
                          <p className="text-gray-600 mb-1">info@ecoguard.ke</p>
                          <p className="text-gray-600">research@ecoguard.ke</p>
                        </div>
                      </div>
                      <div className="flex items-start">
                        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mr-6 flex-shrink-0">
                          <span className="text-3xl">📞</span>
                        </div>
                        <div>
                          <h3 className="text-xl font-bold mb-2 text-gray-900">Phone</h3>
                          <p className="text-gray-600 mb-1">+254 700 123 456</p>
                          <p className="text-gray-600">+254 733 987 654</p>
                        </div>
                      </div>
                      <div className="flex items-start">
                        <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mr-6 flex-shrink-0">
                          <span className="text-3xl">📍</span>
                        </div>
                        <div>
                          <h3 className="text-xl font-bold mb-2 text-gray-900">Office</h3>
                          <p className="text-gray-600 mb-1">Karura Forest Road</p>
                          <p className="text-gray-600">Nairobi, Kenya</p>
                        </div>
                      </div>
                    </div>
                    <div className="mt-12 p-6 bg-green-50 rounded-lg border border-green-200">
                      <h3 className="text-lg font-bold mb-3 text-gray-900">Partnerships</h3>
                      <p className="text-gray-700">
                        Interested in deploying EcoGuard sensors in your forest? Contact us to discuss 
                        partnership opportunities and technical support.
                      </p>
                    </div>
                  </div>
                  <div>
                    <Card className="p-8 border-gray-200 shadow-lg">
                      <h2 className="text-3xl font-bold mb-6 text-gray-900">Send us a Message</h2>
                      <form className="space-y-6" onSubmit={handleFormSubmit}>
                        <div>
                          <label className="block text-sm font-semibold mb-2 text-gray-700">Name</label>
                          <input 
                            type="text" 
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
                            placeholder="Your name"
                            value={formData.name}
                            onChange={(e) => setFormData({...formData, name: e.target.value})}
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-semibold mb-2 text-gray-700">Email</label>
                          <input 
                            type="email" 
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
                            placeholder="your.email@example.com"
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            required
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-semibold mb-2 text-gray-700">Message</label>
                          <textarea 
                            rows={5}
                            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
                            placeholder="How can we help you?"
                            value={formData.message}
                            onChange={(e) => setFormData({...formData, message: e.target.value})}
                            required
                          ></textarea>
                        </div>
                        <Button 
                          type="submit"
                          className="w-full bg-green-600 hover:bg-green-700 text-white py-3 text-lg font-semibold"
                        >
                          Send Message
                        </Button>
                      </form>
                    </Card>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'analytics':
        return (
          <div className="min-h-screen bg-white">
            <div className="container mx-auto px-4 py-16 md:py-20">
              <div className="max-w-6xl mx-auto">
                <div className="text-center mb-12">
                  <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">Analytics Dashboard</h1>
                  <p className="text-xl text-gray-600">Comprehensive data visualization and threat analysis</p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                  <Card className="lg:col-span-2 p-6 border-gray-200 shadow-lg">
                    <h2 className="text-2xl font-bold mb-6 text-gray-900">Threat Detection Overview</h2>
                    <div className="h-80 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                      <div className="text-center">
                        <div className="text-4xl mb-2">📊</div>
                        <p className="text-gray-600">Interactive threat detection chart</p>
                        <p className="text-sm text-gray-500 mt-2">Real-time data visualization coming soon</p>
                      </div>
                    </div>
                  </Card>
                  <Card className="p-6 border-gray-200 shadow-lg">
                    <h2 className="text-2xl font-bold mb-6 text-gray-900">Recent Alerts</h2>
                    <div className="space-y-4">
                      {[
                        { type: 'Chainsaw Detected', location: 'Karura Forest, Sector 7', time: '2 hours ago', priority: 'High' },
                        { type: 'Unusual Activity', location: 'Uhuru Park', time: '5 hours ago', priority: 'Medium' },
                        { type: 'Fire Detected', location: 'Ngong Forest', time: '1 day ago', priority: 'High' },
                        { type: 'Sensor Offline', location: 'Karura Forest, Sector 3', time: '2 days ago', priority: 'Low' },
                      ].map((alert, index) => (
                        <div key={index} className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                          <div className="flex justify-between items-start mb-2">
                            <h3 className="font-bold text-gray-900">{alert.type}</h3>
                            <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                              alert.priority === 'High' ? 'bg-red-100 text-red-800' : 
                              alert.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {alert.priority}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-1">{alert.location}</p>
                          <p className="text-xs text-gray-500">{alert.time}</p>
                        </div>
                      ))}
                    </div>
                  </Card>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <Card className="p-6 border-gray-200 shadow-lg">
                    <h2 className="text-2xl font-bold mb-6 text-gray-900">Forest Health Metrics</h2>
                    <div className="h-64 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                      <div className="text-center">
                        <div className="text-4xl mb-2">🌳</div>
                        <p className="text-gray-600">Forest health visualization</p>
                        <p className="text-sm text-gray-500 mt-2">Coming soon</p>
                      </div>
                    </div>
                  </Card>
                  <Card className="p-6 border-gray-200 shadow-lg">
                    <h2 className="text-2xl font-bold mb-6 text-gray-900">Carbon Credit Tracking</h2>
                    <div className="h-64 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
                      <div className="text-center">
                        <div className="text-4xl mb-2">🌱</div>
                        <p className="text-gray-600">Carbon credit tracking</p>
                        <p className="text-sm text-gray-500 mt-2">Coming soon</p>
                      </div>
                    </div>
                  </Card>
                </div>
              </div>
            </div>
          </div>
        );
      case 'research':
        return (
          <div className="min-h-screen bg-white">
            <div className="container mx-auto px-4 py-16 md:py-20">
              <div className="max-w-6xl mx-auto">
                <div className="text-center mb-12">
                  <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">Research Data Portal</h1>
                  <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                    Access comprehensive datasets for conservation research, climate studies, and policy analysis
                  </p>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                  {[
                    { label: "Datasets Available", value: "24", icon: "📊" },
                    { label: "Total Records", value: "2.4M+", icon: "📈" },
                    { label: "Research Papers", value: "45", icon: "📄" },
                    { label: "Active Partnerships", value: "12", icon: "🤝" },
                  ].map((stat, i) => (
                    <Card key={i} className="text-center p-6 border-gray-200 hover:shadow-lg transition-shadow">
                      <div className="text-3xl mb-2">{stat.icon}</div>
                      <div className="text-3xl font-bold text-green-600 mb-2">{stat.value}</div>
                      <div className="text-gray-600 text-sm">{stat.label}</div>
                    </Card>
                  ))}
                </div>
                
                <div className="mb-12">
                  <h2 className="text-3xl font-bold mb-8 text-gray-900">Dataset Categories</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <Card className="p-6 border-gray-200 hover:shadow-lg transition-shadow">
                      <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
                        <span className="text-3xl">⚠️</span>
                      </div>
                      <h3 className="text-xl font-bold mb-3 text-gray-900">Threat Detection</h3>
                      <p className="text-gray-600 mb-4">Chainsaw detection events, fire monitoring data, and poaching alerts</p>
                      <Button variant="outline" size="sm" className="border-green-600 text-green-600 hover:bg-green-50">
                        Browse Datasets
                      </Button>
                    </Card>
                    <Card className="p-6 border-gray-200 hover:shadow-lg transition-shadow">
                      <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
                        <span className="text-3xl">🌱</span>
                      </div>
                      <h3 className="text-xl font-bold mb-3 text-gray-900">Reforestation</h3>
                      <p className="text-gray-600 mb-4">Seedling growth metrics, planted area performance, and survival rates</p>
                      <Button variant="outline" size="sm" className="border-green-600 text-green-600 hover:bg-green-50">
                        Browse Datasets
                      </Button>
                    </Card>
                    <Card className="p-6 border-gray-200 hover:shadow-lg transition-shadow">
                      <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-4">
                        <span className="text-3xl">🌡️</span>
                      </div>
                      <h3 className="text-xl font-bold mb-3 text-gray-900">Climate Impact</h3>
                      <p className="text-gray-600 mb-4">Carbon storage quantification, biodiversity indicators, and climate data</p>
                      <Button variant="outline" size="sm" className="border-green-600 text-green-600 hover:bg-green-50">
                        Browse Datasets
                      </Button>
                    </Card>
                  </div>
                </div>
                
                <Card className="text-center p-12 bg-gradient-to-r from-green-600 to-emerald-600 text-white border-0 shadow-xl">
                  <h2 className="text-3xl font-bold mb-4">Partner with EcoGuard</h2>
                  <p className="text-xl mb-8 max-w-2xl mx-auto">
                    We're seeking research partnerships with universities, institutions, and government agencies. 
                    Let's advance conservation science together.
                  </p>
                  <div className="flex flex-wrap justify-center gap-4">
                    <Button 
                      size="lg" 
                      className="bg-white text-green-600 hover:bg-gray-100"
                      onClick={() => {
                        if (typeof (window as any).toast === 'function') {
                          (window as any).toast({
                            title: "Access Requested!",
                            description: "We'll contact you with dataset access details.",
                            variant: "success"
                          });
                        }
                      }}
                    >
                      Request Dataset Access
                    </Button>
                    <Button 
                      size="lg" 
                      variant="outline" 
                      className="border-white text-white hover:bg-white/10"
                      onClick={() => {
                        if (typeof (window as any).toast === 'function') {
                          (window as any).toast({
                            title: "Partnership Proposal Submitted!",
                            description: "We'll review your proposal and contact you soon.",
                            variant: "success"
                          });
                        }
                      }}
                    >
                      Propose Partnership
                    </Button>
                  </div>
                </Card>
              </div>
            </div>
          </div>
        );
      default:
        return (
          <div className="min-h-screen bg-background flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-4xl font-bold mb-6">EcoGuard - Modern Forest Protection System</h1>
              <p className="text-lg text-muted-foreground">
                This is the modern React frontend that replaces the current Streamlit interface.
              </p>
            </div>
          </div>
        );
    }
  };

  // If authentication status is still being checked, show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // If user is authenticated, show the requested page (including dashboard)
  if (isAuthenticated) {
    // Allow access to dashboard, analytics, research, and other pages for authenticated users
    const allowedPages = ['home', 'about', 'contact', 'analytics', 'research', 'dashboard', 'signup', 'streamlit'];
    
    // If trying to access a protected page, allow it for authenticated users
    if (allowedPages.includes(currentPage)) {
      return (
        <div className="app min-h-screen bg-white">
          <Navigation 
            currentPage={currentPage} 
            setCurrentPage={handleSetCurrentPage}
            user={user} 
            onLogout={handleLogout} 
          />
          {renderPage()}
        </div>
      );
    }
  }

  // If user is not authenticated, show the requested page
  // (Only home, about, contact, and signup pages are accessible without login)
  if (!isAuthenticated && ['home', 'about', 'contact', 'signup'].includes(currentPage)) {
    return (
      <div className="app min-h-screen bg-background">
        <Navigation 
          currentPage={currentPage} 
          setCurrentPage={handleSetCurrentPage}
          user={user} 
          onLogout={handleLogout} 
        />
        {renderPage()}
      </div>
    );
  }

  // If user is not authenticated and trying to access a protected page, show login page
  return <LoginPage />;
}

export default App;