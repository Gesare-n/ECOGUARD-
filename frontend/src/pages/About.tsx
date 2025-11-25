// Simple About page placeholder
// This would be replaced with a full implementation when dependencies are installed

const About = () => {
  return {
    type: 'div',
    props: {
      className: 'min-h-screen bg-background',
      children: [
        // Navigation would go here
        {
          type: 'div',
          props: {
            className: 'pt-24 pb-12',
            children: [
              // Hero Section
              {
                type: 'section',
                props: {
                  className: 'relative h-96 mb-12 overflow-hidden',
                  children: [
                    {
                      type: 'div',
                      props: {
                        className: 'absolute inset-0 bg-cover bg-center',
                        style: { backgroundImage: 'url(https://placehold.co/1200x400/065f46/ffffff?text=EcoGuard+Hero)' },
                        children: {
                          type: 'div',
                          props: {
                            className: 'absolute inset-0 bg-gradient-to-r from-primary/90 to-primary/60'
                          }
                        }
                      }
                    },
                    {
                      type: 'div',
                      props: {
                        className: 'container mx-auto px-4 h-full flex items-center relative z-10',
                        children: {
                          type: 'div',
                          props: {
                            className: 'max-w-2xl',
                            children: [
                              {
                                type: 'h1',
                                props: {
                                  className: 'text-5xl md:text-6xl font-serif font-bold text-primary-foreground mb-4',
                                  children: 'About EcoGuard'
                                }
                              },
                              {
                                type: 'p',
                                props: {
                                  className: 'text-xl text-primary-foreground/90',
                                  children: 'Protecting Kenya\'s forests through innovation, inspired by Wangari Maathai\'s legacy'
                                }
                              }
                            ]
                          }
                        }
                      }
                    }
                  ]
                }
              },
              // Content sections would go here
              {
                type: 'div',
                props: {
                  className: 'container mx-auto px-4',
                  children: [
                    {
                      type: 'h2',
                      props: {
                        className: 'text-3xl font-bold mb-6',
                        children: 'Our Mission and Vision'
                      }
                    },
                    {
                      type: 'p',
                      props: {
                        className: 'text-lg mb-6',
                        children: 'To protect Kenya\'s forests through AI-powered threat detection, verified reforestation, and sustainable carbon credit systems. We combine cutting-edge technology with local conservation efforts to create lasting environmental impact.'
                      }
                    },
                    {
                      type: 'h2',
                      props: {
                        className: 'text-3xl font-bold mb-6 mt-12',
                        children: 'Inspired by Wangari Maathai'
                      }
                    },
                    {
                      type: 'p',
                      props: {
                        className: 'text-lg mb-6',
                        children: 'Professor Wangari Maathai\'s Green Belt Movement planted over 51 million trees across Kenya, empowering communities and restoring ecosystems. Her vision of environmental conservation combined with social justice continues to inspire our work.'
                      }
                    },
                    {
                      type: 'h2',
                      props: {
                        className: 'text-3xl font-bold mb-6 mt-12',
                        children: 'Our Technology'
                      }
                    },
                    {
                      type: 'p',
                      props: {
                        className: 'text-lg mb-6',
                        children: 'Solar-powered, autonomous sensors equipped with advanced ML models and long-range connectivity'
                      }
                    },
                    {
                      type: 'ul',
                      props: {
                        className: 'list-disc list-inside mb-6',
                        children: [
                          { type: 'li', props: { children: 'Solar-powered with 7-day battery backup' } },
                          { type: 'li', props: { children: 'IP67 weatherproof rating for harsh conditions' } },
                          { type: 'li', props: { children: 'High-fidelity microphone array for sound detection' } },
                          { type: 'li', props: { children: '4K camera for visual monitoring' } },
                          { type: 'li', props: { children: 'LoRa mesh networking (10km+ range)' } },
                          { type: 'li', props: { children: 'Edge computing for real-time processing' } }
                        ]
                      }
                    }
                  ]
                }
              }
            ]
          }
        }
      ]
    }
  };
};

export default About;