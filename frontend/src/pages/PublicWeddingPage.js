import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAppTheme } from '../App';
import { Calendar, MapPin, Heart, Clock, User, MessageCircle, Camera } from 'lucide-react';

// Import Navigation and FloatingTemplateButton to make it exactly like the main site
import Navigation from '../components/Navigation';
import FloatingTemplateButton from '../components/FloatingTemplateButton';

// Default wedding data for fallback (complete data structure)
const defaultWeddingData = {
  couple_name_1: 'Sarah',
  couple_name_2: 'Michael',
  wedding_date: '2025-06-15',
  venue_name: 'Sunset Garden Estate',
  venue_location: 'Sunset Garden Estate • Napa Valley, California',
  their_story: 'We can\'t wait to celebrate our love story with the people who matter most to us. Join us for an unforgettable evening of joy, laughter, and new beginnings.',
  theme: 'classic',
  
  // Complete data structure from UserDataContext
  story_timeline: [
    {
      year: "2019",
      title: "First Meeting",
      description: "We met at a coffee shop in downtown San Francisco on a rainy Tuesday morning. Sarah ordered a lavender latte, and Michael couldn't stop staring at her beautiful smile.",
      image: "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=600&h=400&fit=crop"
    },
    {
      year: "2020", 
      title: "First Date",
      description: "Our first official date was a sunset picnic in Golden Gate Park. We talked for hours about our dreams, travels, and favorite books under the stars.",
      image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=600&h=400&fit=crop"
    },
    {
      year: "2021",
      title: "Moving In Together", 
      description: "After a year of long-distance dating, we decided to take the next step and move in together. Our first apartment was tiny but filled with so much love.",
      image: "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=600&h=400&fit=crop"
    },
    {
      year: "2023",
      title: "The Proposal",
      description: "Michael proposed during our vacation in Santorini, Greece. As the sun set over the Aegean Sea, he got down on one knee with Sarah's grandmother's ring.",
      image: "https://images.unsplash.com/photo-1597248374161-426f3d6f1f6b?w=600&h=400&fit=crop"
    },
    {
      year: "2025",
      title: "Our Wedding Day",
      description: "And now, we're ready to say 'I do' surrounded by our family and friends. This is just the beginning of our beautiful journey together.",
      image: "https://images.unsplash.com/photo-1519741497674-611481863552?w=600&h=400&fit=crop"
    }
  ],
  
  schedule_events: [
    {
      time: "2:00 PM",
      title: "Guests Arrival & Welcome",
      description: "Please arrive by 2:00 PM for welcome drinks and mingling before the ceremony begins.",
      location: "Sunset Garden Estate - Main Entrance",
      icon: "Users",
      duration: "30 minutes"
    },
    {
      time: "2:30 PM",
      title: "Pre-Ceremony Music",
      description: "Enjoy live acoustic music as guests are seated for the ceremony.",
      location: "Garden Ceremony Space",
      icon: "Music",
      duration: "30 minutes"
    },
    {
      time: "3:00 PM",
      title: "Wedding Ceremony",
      description: "The main event! Wedding ceremony with exchange of vows in our beautiful garden setting.",
      location: "Sunset Garden Estate - Ceremony Garden",
      icon: "Calendar",
      duration: "45 minutes",
      highlight: true
    },
    {
      time: "3:45 PM",
      title: "Cocktail Hour & Photos",
      description: "Celebrate with signature cocktails while the wedding party takes photos.",
      location: "Terrace & Garden Areas",
      icon: "Camera",
      duration: "1 hour 15 minutes"
    },
    {
      time: "5:00 PM",
      title: "Reception Dinner",
      description: "Join us for a three-course dinner featuring locally sourced ingredients.",
      location: "Grand Ballroom",
      icon: "Utensils",
      duration: "2 hours"
    },
    {
      time: "7:30 PM",
      title: "First Dance & Toasts",
      description: "Watch the newlyweds' first dance followed by heartfelt toasts from family and friends.",
      location: "Grand Ballroom",
      icon: "Music",
      duration: "30 minutes"
    },
    {
      time: "8:00 PM",
      title: "Dancing & Celebration",
      description: "Dance the night away with live music and DJ entertainment.",
      location: "Grand Ballroom & Terrace",
      icon: "Music",
      duration: "4 hours"
    }
  ]
};

const PublicWeddingPage = () => {
  const params = useParams();
  const { themes } = useAppTheme();
  const [currentTheme, setTheme] = useState('classic');
  const theme = themes[currentTheme];
  
  // Get URL parameter - could be customUrl or the catch-all
  const customUrl = params.customUrl || params['*'];
  const weddingId = params.weddingId;
  
  console.log('PublicWeddingPage - URL Params:', params);
  console.log('PublicWeddingPage - Extracted customUrl:', customUrl);
  console.log('PublicWeddingPage - Extracted weddingId:', weddingId);
  
  const [weddingData, setWeddingData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  });

  useEffect(() => {
    loadWeddingData();
  }, [customUrl, weddingId]);

  useEffect(() => {
    if (weddingData && weddingData.wedding_date) {
      const timer = setInterval(() => {
        const weddingDate = new Date(weddingData.wedding_date + 'T15:00:00');
        const now = new Date().getTime();
        const distance = weddingDate.getTime() - now;

        if (distance > 0) {
          setTimeLeft({
            days: Math.floor(distance / (1000 * 60 * 60 * 24)),
            hours: Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
            minutes: Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)),
            seconds: Math.floor((distance % (1000 * 60)) / 1000)
          });
        }
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [weddingData]);

  useEffect(() => {
    if (weddingData && weddingData.theme) {
      setTheme(weddingData.theme);
    }
  }, [weddingData]);

  const loadWeddingData = async () => {
    try {
      setLoading(true);
      
      // Get the identifier from URL params
      const identifier = customUrl || weddingId;
      let foundWeddingData = null;
      
      console.log('Loading wedding data for identifier:', identifier);
      
      if (identifier) {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
        
        try {
          // First try to fetch from backend by custom URL
          if (customUrl) {
            console.log('Trying to fetch by custom URL:', customUrl);
            const response = await fetch(`${backendUrl}/api/wedding/public/custom/${identifier}`);
            if (response.ok) {
              foundWeddingData = await response.json();
              console.log('Found wedding data by custom URL:', foundWeddingData);
            } else {
              console.log('Custom URL not found in backend, response:', response.status);
            }
          } else {
            // Try to fetch by user ID
            console.log('Trying to fetch by user ID:', identifier);
            const response = await fetch(`${backendUrl}/api/wedding/public/user/${identifier}`);
            if (response.ok) {
              foundWeddingData = await response.json();
              console.log('Found wedding data by user ID:', foundWeddingData);
            } else {
              console.log('User ID not found in backend, response:', response.status);
            }
          }
        } catch (backendError) {
          console.log('Backend fetch failed, trying localStorage fallback:', backendError);
        }
        
        // Fallback to localStorage if backend fails
        if (!foundWeddingData) {
          console.log('Trying localStorage fallback');
          console.log('Identifier to search for:', identifier);
          
          const storedUsers = localStorage.getItem('wedding_users');
          console.log('Stored users from localStorage:', storedUsers);
          
          if (storedUsers) {
            const users = JSON.parse(storedUsers);
            console.log('Parsed users:', users);
            
            // Search for user by ID or custom URL
            for (const userId in users) {
              console.log('Checking user ID:', userId);
              const userData = localStorage.getItem(`wedding_data_${userId}`);
              console.log(`Wedding data for ${userId}:`, userData);
              
              if (userData) {
                const userWeddingData = JSON.parse(userData);
                console.log('Parsed user wedding data:', userWeddingData);
                console.log('Custom URL in data:', userWeddingData.custom_url);
                
                // Match by user ID or custom URL
                if (userId === identifier || userWeddingData.custom_url === identifier) {
                  foundWeddingData = userWeddingData;
                  console.log('✅ MATCH FOUND! Found wedding data in localStorage:', foundWeddingData);
                  break;
                } else {
                  console.log(`❌ No match: ${userId} !== ${identifier} && ${userWeddingData.custom_url} !== ${identifier}`);
                }
              }
            }
          } else {
            console.log('❌ No users found in localStorage');
          }
          
          if (!foundWeddingData) {
            console.log('❌ No matching wedding data found in localStorage');
          }
        }
      }
      
      if (foundWeddingData) {
        // Merge with default data to ensure all sections are available
        const mergedData = { ...defaultWeddingData, ...foundWeddingData };
        setWeddingData(mergedData);
        console.log('Final wedding data set:', mergedData);
      } else {
        // Fallback to default data if no user data found
        console.log('No wedding data found, using default data');
        setWeddingData(defaultWeddingData);
      }
      
    } catch (error) {
      console.error('Error loading wedding data:', error);
      // Use default data as fallback
      setWeddingData(defaultWeddingData);
    } finally {  
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center"
        style={{ 
          background: theme.gradientPrimary,
          fontFamily: theme.fontSecondary 
        }}
      >
        <div className="text-center">
          <Heart className="w-16 h-16 mx-auto mb-4 animate-pulse" style={{ color: theme.accent }} />
          <p className="text-xl" style={{ color: theme.text }}>Loading wedding invitation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center"
        style={{ 
          background: theme.gradientPrimary,
          fontFamily: theme.fontSecondary 
        }}
      >
        <div className="text-center">
          <Heart className="w-16 h-16 mx-auto mb-4" style={{ color: theme.textLight }} />
          <h1 className="text-2xl font-semibold mb-2" style={{ color: theme.primary }}>
            Wedding Invitation Not Found
          </h1>
          <p className="text-lg" style={{ color: theme.textLight }}>{error}</p>
        </div>
      </div>
    );
  }

  // Render the complete wedding website exactly like the main site
  return (
    <div 
      className="min-h-screen"
      style={{
        background: themes[currentTheme].background,
        color: themes[currentTheme].text,
        fontFamily: themes[currentTheme].fontSecondary,
      }}
    >
      {/* Navigation - same as main site */}
      <Navigation />
      
      {/* Floating Template Button - same as main site */}
      <FloatingTemplateButton />
      
      {/* Main Content - Homepage layout with personalized data */}
      <div 
        className="min-h-screen"
        style={{
          background: `linear-gradient(135deg, ${theme.secondary}80 0%, ${theme.background}90 50%, ${theme.accent}10 100%)`,
          fontFamily: theme.fontSecondary
        }}
      >
        {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="max-w-4xl mx-auto px-4 py-16 text-center">
            <div className="mb-8">
              <Heart className="w-20 h-20 mx-auto mb-6 animate-pulse" style={{ color: theme.accent }} />
              <h1 
                className="text-6xl md:text-8xl font-light mb-4"
                style={{ 
                  fontFamily: theme.fontPrimary,
                  color: theme.primary,
                  background: theme.gradientAccent,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent'
                }}
              >
                {weddingData?.couple_name_1} & {weddingData?.couple_name_2}
              </h1>
              
              {weddingData?.wedding_date && (
                <p className="text-2xl md:text-3xl mb-4" style={{ color: theme.textLight }}>
                  {formatDate(weddingData.wedding_date)}
                </p>
              )}
              
              {weddingData?.venue_location && (
                <p className="text-lg flex items-center justify-center space-x-2" style={{ color: theme.text }}>
                  <MapPin className="w-5 h-5" />
                  <span>{weddingData.venue_location}</span>
                </p>
              )}
            </div>

            {/* Countdown */}
            {timeLeft.days > 0 && (
              <div className="bg-white/40 backdrop-blur-xl rounded-3xl p-8 border border-white/30 mb-12">
                <h2 className="text-2xl font-semibold mb-6" style={{ color: theme.primary }}>
                  Counting Down to Our Special Day
                </h2>
                <div className="grid grid-cols-4 gap-4">
                  {Object.entries(timeLeft).map(([unit, value]) => (
                    <div key={unit} className="text-center">
                      <div 
                        className="text-4xl md:text-5xl font-bold"
                        style={{ color: theme.accent }}
                      >
                        {value}
                      </div>
                      <div 
                        className="text-sm uppercase tracking-wide font-medium"
                        style={{ color: theme.textLight }}
                      >
                        {unit}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Love Story */}
        {weddingData?.their_story && (
          <div className="max-w-4xl mx-auto px-4 py-16">
            <div className="bg-white/40 backdrop-blur-xl rounded-3xl p-8 border border-white/30">
              <h2 
                className="text-3xl font-light mb-6 text-center"
                style={{ 
                  fontFamily: theme.fontPrimary,
                  color: theme.primary 
                }}
              >
                Our Love Story
              </h2>
              <p 
                className="text-lg leading-relaxed text-center max-w-3xl mx-auto"
                style={{ color: theme.text }}
              >
                {weddingData.their_story}
              </p>
            </div>
          </div>
        )}

        {/* Schedule */}
        {weddingData?.schedule_events && weddingData.schedule_events.length > 0 && (
          <div className="max-w-4xl mx-auto px-4 py-16">
            <div className="bg-white/40 backdrop-blur-xl rounded-3xl p-8 border border-white/30">
              <h2 
                className="text-3xl font-light mb-8 text-center"
                style={{ 
                  fontFamily: theme.fontPrimary,
                  color: theme.primary 
                }}
              >
                Wedding Day Schedule
              </h2>
              <div className="space-y-6">
                {weddingData.schedule_events.map((event, index) => (
                  <div key={index} className="flex items-start space-x-4 p-4 bg-white/30 backdrop-blur-lg rounded-2xl">
                    <div className="flex-shrink-0">
                      <div 
                        className="w-12 h-12 rounded-full flex items-center justify-center"
                        style={{ background: theme.gradientAccent }}
                      >
                        <Clock className="w-6 h-6 text-white" />
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold" style={{ color: theme.primary }}>
                          {event.title}
                        </h3>
                        <span className="text-sm font-medium" style={{ color: theme.accent }}>
                          {event.time}
                        </span>
                      </div>
                      {event.description && (
                        <p className="text-sm mb-2" style={{ color: theme.text }}>
                          {event.description}
                        </p>
                      )}
                      {event.location && (
                        <p className="text-sm flex items-center space-x-1" style={{ color: theme.textLight }}>
                          <MapPin className="w-3 h-3" />
                          <span>{event.location}</span>
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center py-16">
          <Heart className="w-12 h-12 mx-auto mb-4" style={{ color: theme.accent }} />
          <p className="text-lg" style={{ color: theme.textLight }}>
            Thank you for celebrating with us!
          </p>
          <p className="text-sm mt-2" style={{ color: theme.textLight }}>
            {weddingData?.couple_name_1} & {weddingData?.couple_name_2}
          </p>
        </div>
      </div>
    </div>
  );
};

export default PublicWeddingPage;