// Organization signup form for EcoGuard

import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { useToast } from '../components/ui/toast';

const OrganizationSignup = () => {
  const { toast } = useToast();
  const [formData, setFormData] = useState({
    organizationName: '',
    contactPerson: '',
    email: '',
    phone: '',
    region: '',
    forestTypes: [] as string[],
    description: ''
  });
  const [loading, setLoading] = useState(false);

  const forestTypeOptions = [
    'Montane Forests (Mau, Aberdares, Mount Kenya)',
    'Tropical Rainforest (Kakamega)',
    'Dry Deciduous Forest (Rift Valley, Samburu)',
    'Woodland Savanna (Tsavo, Amboseli)'
  ];

  const regionOptions = [
    'Nairobi',
    'Central Kenya',
    'Coast',
    'Rift Valley',
    'Western Kenya',
    'Northern Kenya',
    'Other'
  ];

  const handleForestTypeChange = (type: string) => {
    setFormData(prev => {
      const newForestTypes = prev.forestTypes.includes(type)
        ? prev.forestTypes.filter(t => t !== type)
        : [...prev.forestTypes, type];
      
      return {
        ...prev,
        forestTypes: newForestTypes
      };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.organizationName || !formData.contactPerson || !formData.email || 
        !formData.phone || !formData.region || formData.forestTypes.length === 0) {
      toast({
        title: "Error",
        description: "Please fill in all required fields",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);
    
    try {
      // In a real app, this would send the form data to a server
      console.log('Organization signup data:', formData);
      
      // Show success toast
      toast({
        title: "Application Submitted!",
        description: "We'll review your application and contact you within 3 business days.",
        variant: "success"
      });
      
      // Reset form
      setFormData({
        organizationName: '',
        contactPerson: '',
        email: '',
        phone: '',
        region: '',
        forestTypes: [],
        description: ''
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to submit application. Please try again.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary">
      <div className="container mx-auto px-4 py-8 md:py-16">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8 md:mb-12">
            <h1 className="text-3xl md:text-4xl font-bold mb-4">Organization Registration</h1>
            <p className="text-base md:text-lg text-muted-foreground">
              Join EcoGuard to help protect Kenya's forests
            </p>
          </div>

          <Card className="p-6 md:p-8">
            <form onSubmit={handleSubmit} className="space-y-6 md:space-y-8">
              <div>
                <h2 className="text-xl md:text-2xl font-bold mb-4 md:mb-6">Organization Information</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Organization Name <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.organizationName}
                      onChange={(e) => setFormData({...formData, organizationName: e.target.value})}
                      className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                      placeholder="Enter organization name"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Contact Person <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.contactPerson}
                      onChange={(e) => setFormData({...formData, contactPerson: e.target.value})}
                      className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                      placeholder="Full name"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Email <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                      placeholder="organization@example.com"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Phone <span className="text-destructive">*</span>
                    </label>
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value})}
                      className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                      placeholder="+254 700 123 456"
                      required
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-6">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Region <span className="text-destructive">*</span>
                    </label>
                    <select
                      value={formData.region}
                      onChange={(e) => setFormData({...formData, region: e.target.value})}
                      className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                      required
                    >
                      <option value="">Select region</option>
                      {regionOptions.map(region => (
                        <option key={region} value={region}>{region}</option>
                      ))}
                    </select>
                  </div>
                </div>
                
                <div className="mb-6">
                  <label className="block text-sm font-medium mb-2">
                    Forest Types <span className="text-destructive">*</span>
                  </label>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {forestTypeOptions.map(type => (
                      <div key={type} className="flex items-center">
                        <input
                          type="checkbox"
                          id={type}
                          checked={formData.forestTypes.includes(type)}
                          onChange={() => handleForestTypeChange(type)}
                          className="h-4 w-4 text-primary focus:ring-primary border-input rounded"
                        />
                        <label htmlFor={type} className="ml-2 text-sm">
                          {type}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">
                    Description
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={4}
                    className="w-full px-3 py-2 md:px-4 md:py-2 border border-input rounded-lg focus:ring-2 focus:ring-primary focus:border-primary bg-background"
                    placeholder="Tell us about your organization and conservation efforts..."
                  ></textarea>
                </div>
              </div>
              
              <div className="bg-muted rounded-lg p-4 md:p-6">
                <h3 className="font-bold mb-2">Application Process</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  After submitting your application, our team will review your information. 
                  We'll contact you within 3 business days to discuss next steps.
                </p>
                <ul className="text-xs md:text-sm text-muted-foreground space-y-1">
                  <li className="flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span>Applications are reviewed by our regional coordinators</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span>We may contact you for additional information</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span>Approval typically takes 5-10 business days</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-primary mr-2">•</span>
                    <span>Approved organizations receive access to our dashboard and resources</span>
                  </li>
                </ul>
              </div>
              
              <Button 
                type="submit" 
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                    Submitting...
                  </span>
                ) : (
                  "Submit Application"
                )}
              </Button>
            </form>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default OrganizationSignup;