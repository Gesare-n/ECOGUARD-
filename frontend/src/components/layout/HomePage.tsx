import { useState } from 'react';
import { Button } from '../ui/button';
import { Card } from '../ui/card';

const HomePage = ({ setCurrentPage }: { setCurrentPage: (page: string) => void }) => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Newsletter submitted:', { firstName, lastName, email });
    setFirstName('');
    setLastName('');
    setEmail('');
    if (typeof (window as any).toast === 'function') {
      (window as any).toast({
        title: "Thank you!",
        description: "We'll keep you updated on our progress.",
        variant: "success"
      });
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section - With Hummingbird Theme */}
      <section className="relative bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 py-20 md:py-32">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="mb-6">
              <div className="inline-block text-6xl md:text-8xl mb-4">🐦</div>
              <p className="text-sm md:text-base text-gray-600 font-semibold mb-2">The Digital Hummingbird</p>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Protecting Kenya's Forests
            </h1>
            <p className="text-xl md:text-2xl text-gray-700 mb-4 max-w-2xl mx-auto">
              Like the hummingbird, we do the best we can.
            </p>
            <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              AI-powered acoustic monitoring system detecting illegal logging, wildfires, and threats in real-time. 
              Small sensors, big impact.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Button 
                size="lg" 
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-6 text-lg font-semibold rounded-lg shadow-lg"
                onClick={() => setCurrentPage('signup')}
              >
                Get Started
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="px-8 py-6 text-lg font-semibold border-2 border-gray-900 hover:bg-gray-50"
                onClick={() => setCurrentPage('about')}
              >
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">The Problem</h2>
              <h3 className="text-2xl md:text-3xl font-semibold text-gray-700 mb-4">
                Illegal logging, wildfires, and deforestation threaten Kenya's forests
              </h3>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Kenya's protected forests face constant threats from illegal logging, poaching, and wildfires. 
                Traditional monitoring methods are insufficient to detect and respond to these threats in time. 
                By the time rangers discover illegal activity, significant damage has often already occurred.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card className="p-6 text-center border-gray-200">
                <div className="text-4xl mb-4">🪓</div>
                <h3 className="text-xl font-bold mb-2">Illegal Logging</h3>
                <p className="text-gray-600">Chainsaw activity detected in protected areas</p>
              </Card>
              <Card className="p-6 text-center border-gray-200">
                <div className="text-4xl mb-4">🔥</div>
                <h3 className="text-xl font-bold mb-2">Wildfires</h3>
                <p className="text-gray-600">Uncontrolled fires destroying forest ecosystems</p>
              </Card>
              <Card className="p-6 text-center border-gray-200">
                <div className="text-4xl mb-4">🌳</div>
                <h3 className="text-xl font-bold mb-2">Deforestation</h3>
                <p className="text-gray-600">Rapid loss of forest cover and biodiversity</p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* The Solution Section - Digital Hummingbird */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <div className="text-6xl mb-4">🐦</div>
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">The Digital Hummingbird Solution</h2>
              <h3 className="text-2xl md:text-3xl font-semibold text-gray-700 mb-4">
                Small sensors doing the best they can
              </h3>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Inspired by Wangari Maathai's hummingbird story, EcoGuard uses small, solar-powered acoustic sensors 
                that work tirelessly to detect threats. Like the hummingbird that tried to put out the forest fire 
                one drop at a time, our sensors may be small, but they do the best they can to protect our forests.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
              <div>
                <h3 className="text-2xl font-bold mb-4">How It Works</h3>
                <ul className="space-y-4">
                  <li className="flex items-start">
                    <span className="text-green-600 mr-3 text-xl">✓</span>
                    <div>
                      <strong className="block">AI-Powered Detection</strong>
                      <p className="text-gray-600">TensorFlow Lite models detect chainsaw sounds with {'>'}90% accuracy</p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-600 mr-3 text-xl">✓</span>
                    <div>
                      <strong className="block">Instant SMS Alerts</strong>
                      <p className="text-gray-600">Rangers receive immediate notifications with GPS coordinates</p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-600 mr-3 text-xl">✓</span>
                    <div>
                      <strong className="block">Solar-Powered & Autonomous</strong>
                      <p className="text-gray-600">5-10 year battery life with solar recharging, operates in remote locations</p>
                    </div>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-600 mr-3 text-xl">✓</span>
                    <div>
                      <strong className="block">LoRa Communication</strong>
                      <p className="text-gray-600">Long-range wireless mesh network up to 20km range</p>
                    </div>
                  </li>
                </ul>
              </div>
              <div className="bg-green-100 rounded-2xl p-8 md:p-12 text-center">
                <div className="text-8xl mb-4">🐦</div>
                <h4 className="text-xl font-bold mb-2">The Digital Hummingbird</h4>
                <p className="text-gray-700">
                  Raspberry Pi-based sensor in a bird-shaped enclosure, monitoring forests 24/7
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Impact Metrics */}
      <section className="py-20 bg-green-600 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-16">By the numbers</h2>
            <h3 className="text-2xl md:text-3xl font-semibold text-center mb-12">Protecting People & Planet</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold mb-4">12+</div>
                <div className="text-xl md:text-2xl">Forests Protected</div>
              </div>
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold mb-4">287</div>
                <div className="text-xl md:text-2xl">Threats Detected</div>
              </div>
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold mb-4">3,500+</div>
                <div className="text-xl md:text-2xl">Hectares Monitored</div>
              </div>
              <div className="text-center">
                <div className="text-5xl md:text-6xl font-bold mb-4">12.4K</div>
                <div className="text-xl md:text-2xl">Tons CO₂ Saved</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Features */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 text-gray-900">System Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card className="p-8 text-center hover:shadow-lg transition-shadow border-gray-200">
                <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">🌳</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Real-Time Monitoring</h3>
                <p className="text-gray-600">
                  Interactive forest maps with live sensor data and threat visualization
                </p>
              </Card>
              <Card className="p-8 text-center hover:shadow-lg transition-shadow border-gray-200">
                <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">📡</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Instant Alerts</h3>
                <p className="text-gray-600">
                  SMS notifications to rangers with GPS coordinates for rapid response
                </p>
              </Card>
              <Card className="p-8 text-center hover:shadow-lg transition-shadow border-gray-200">
                <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-6">
                  <span className="text-3xl">📊</span>
                </div>
                <h3 className="text-2xl font-bold mb-4">Data Analytics</h3>
                <p className="text-gray-600">
                  Comprehensive dashboards for rangers, managers, and researchers
                </p>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <div className="text-6xl mb-6">🐦</div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Join the Digital Hummingbird Movement</h2>
            <p className="text-xl md:text-2xl text-gray-300 mb-8">
              Like the hummingbird, we may be small, but we do the best we can.
            </p>
            <p className="text-lg md:text-xl mb-12">
              Protect more forests and change more lives with us.
            </p>
            <Button 
              size="lg" 
              className="bg-green-600 hover:bg-green-700 text-white px-12 py-6 text-lg font-semibold rounded-lg shadow-lg"
              onClick={() => setCurrentPage('signup')}
            >
              Support Our Work
            </Button>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4 text-gray-900">Add Impact to Your Inbox</h2>
            <form onSubmit={handleSubmit} className="mt-8 flex flex-col sm:flex-row gap-4">
              <input
                type="text"
                placeholder="First Name *"
                required
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              <input
                type="text"
                placeholder="Last Name *"
                required
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              <input
                type="email"
                placeholder="Email Address *"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
              <Button 
                type="submit"
                className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 font-semibold rounded-lg"
              >
                Submit
              </Button>
            </form>
            <p className="text-sm text-gray-600 mt-4">
              Get our emails to stay in the know on what's happening in the field and ways you can get involved.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;