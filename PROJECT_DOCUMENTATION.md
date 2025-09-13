# Wedding Card Website - Complete Project Documentation

## 🚀 Project Overview
**Project Name**: Premium Wedding Card Website  
**Tech Stack**: React + FastAPI + MongoDB  
**Type**: Full-stack responsive wedding website with premium UI/UX  
**Current Status**: Mobile Navigation Enhancement Phase  

---

## 📁 Project Structure

```
/app/
├── backend/                    # FastAPI Backend
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Backend environment variables
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── App.js             # Main React component with routing
│   │   ├── App.css            # Global styles and animations
│   │   ├── index.js           # Entry point
│   │   ├── components/
│   │   │   ├── Navigation.js  # **MAIN NAVIGATION COMPONENT** (Currently being enhanced)
│   │   │   ├── FloatingTemplateButton.js
│   │   │   ├── TemplateCustomizer.js
│   │   │   ├── LiquidBackground.js
│   │   │   └── ui/            # Radix UI components
│   │   ├── pages/             # Page components
│   │   │   ├── HomePage.js
│   │   │   ├── RSVPPage.js
│   │   │   ├── StoryPage.js
│   │   │   ├── GalleryPage.js
│   │   │   ├── PartyPage.js
│   │   │   ├── SchedulePage.js
│   │   │   ├── RegistryPage.js
│   │   │   ├── FAQPage.js
│   │   │   └── GuestbookPage.js
│   │   ├── hooks/             # Custom React hooks
│   │   └── lib/               # Utility functions
│   ├── package.json           # Dependencies and scripts
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   └── postcss.config.js      # PostCSS configuration
└── tests/                     # Test files
```

---

## 🎨 Current Features & Functionality

### ✅ Completed Features
1. **Multi-Theme System**: Classic, Modern, Boho themes
2. **Responsive Design**: Desktop and mobile layouts
3. **Page Navigation**: 9 main pages with React Router
4. **Theme Context**: Global theme management
5. **Basic Mobile Menu**: Simple dropdown navigation
6. **Custom Animations**: CSS keyframes for smooth transitions
7. **Glass Morphism**: Backdrop blur effects
8. **Custom Scrollbar**: Themed scrollbar styling

### 🔄 Current Development Phase
**Mobile Navigation Enhancement** - Creating world-class premium mobile navbar with:
- Full-screen overlay with blur backdrop
- Smooth slide-in animations
- Enhanced click-outside functionality
- Modern visual effects and micro-interactions
- Proper z-index layering to prevent overlap

---

## 🛠 Technical Implementation Details

### Frontend Architecture
- **Framework**: React 19.0.0
- **Routing**: React Router DOM 7.5.1
- **Styling**: Tailwind CSS 3.4.17 + Custom CSS
- **UI Components**: Radix UI ecosystem
- **Animations**: Framer Motion 12.23.12 + Custom CSS animations
- **Icons**: Lucide React 0.507.0
- **Build Tool**: Create React App with CRACO

### Backend Architecture
- **Framework**: FastAPI 0.110.1
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with python-jose
- **Environment**: Python-dotenv for configuration

### Key Dependencies
```json
"react": "^19.0.0",
"react-router-dom": "^7.5.1",
"framer-motion": "^12.23.12",
"lucide-react": "^0.507.0",
"tailwindcss": "^3.4.17",
"@radix-ui/*": "Latest versions"
```

---

## 🎭 Theme System

### Theme Structure
```javascript
themes = {
  classic: {
    primary: '#1a1a1a',
    secondary: '#f8f6f0', 
    accent: '#d4af37',
    fontPrimary: "'Playfair Display', serif",
    fontSecondary: "'Inter', sans-serif"
  },
  modern: {
    primary: '#2c2c2c',
    accent: '#ff6b6b',
    fontPrimary: "'Montserrat', sans-serif"
  },
  boho: {
    primary: '#8b4513',
    accent: '#cd853f',
    fontPrimary: "'Dancing Script', cursive"
  }
}
```

### Theme Usage
- Context Provider in App.js manages global theme state
- All components use `useAppTheme()` hook to access current theme
- Dynamic styling with inline styles for theme-specific colors

---

## 📱 Navigation System (Current Focus)

### Current Navigation Component (`/frontend/src/components/Navigation.js`)
**Location**: `/app/frontend/src/components/Navigation.js`  
**Status**: Under Enhancement  

#### Current Features:
- Fixed positioned navbar with scroll-based transparency
- Desktop horizontal navigation
- Basic mobile dropdown menu
- Theme selector integration
- Click-outside detection (basic implementation)

#### Known Issues Being Fixed:
1. **Overlap Problem**: Mobile menu overlaps with background content
2. **Z-index Issues**: Menu doesn't properly layer above all content  
3. **Basic Design**: Current mobile menu lacks premium feel
4. **Limited Animations**: Simple show/hide without smooth transitions

#### Navigation Items:
```javascript
navItems = [
  { path: '/', label: 'Home' },
  { path: '/story', label: 'Our Story' },
  { path: '/rsvp', label: 'RSVP' },
  { path: '/schedule', label: 'Schedule' },
  { path: '/gallery', label: 'Gallery' },
  { path: '/party', label: 'Wedding Party' },
  { path: '/registry', label: 'Registry' },
  { path: '/guestbook', label: 'Guestbook' },
  { path: '/faq', label: 'FAQ' }
]
```

---

## 🎯 Development Workflow

### Setup Commands
```bash
# Frontend setup
cd /app/frontend && yarn install

# Backend setup  
cd /app/backend && pip install -r requirements.txt

# Start all services
sudo supervisorctl restart all
```

### Service Management
- **Frontend**: Runs on port 3000 with hot reload
- **Backend**: Runs on port 8001 with auto-restart
- **MongoDB**: Local database instance
- **Services**: Managed via supervisorctl

### Development Guidelines
1. **Hot Reload**: Both frontend and backend support hot reload
2. **Theme Integration**: All new components must use theme context
3. **Responsive Design**: Mobile-first approach with Tailwind classes
4. **Animations**: Use combination of Framer Motion and custom CSS
5. **State Management**: React Context for global state

---

## 🚀 Deployment & Environment

### Environment Variables
```bash
# Frontend (.env)
REACT_APP_BACKEND_URL=<backend_url>

# Backend (.env)  
MONGO_URL=<mongodb_connection_string>
```

### Build Commands
```bash
# Frontend build
cd /app/frontend && yarn build

# Production deployment
# Uses CRACO for custom webpack configuration
```

---

## 📋 Testing Strategy

### Current Testing Setup
- **Framework**: Jest (via Create React App)
- **Component Testing**: React Testing Library
- **Backend Testing**: Pytest
- **E2E Testing**: Playwright (via deep_testing_cloud agent)

### Test Commands
```bash
# Frontend tests
cd /app/frontend && yarn test

# Backend tests
cd /app/backend && pytest
```

---

## 🔮 Future AI Agent Instructions

### For Mobile Navigation Enhancement:
1. **Focus File**: `/app/frontend/src/components/Navigation.js`
2. **Key Requirements**: 
   - Full-screen overlay (z-index: 9999)
   - Blur backdrop-filter
   - Slide-in animations from right/left
   - Click-outside functionality enhancement
   - Premium visual effects

### For New Feature Development:
1. **Always use theme context**: Import `useAppTheme()` from '../App'
2. **Follow responsive pattern**: Desktop-first navigation, mobile overlay
3. **Maintain consistency**: Use existing animation classes from App.css
4. **Test thoroughly**: Use deep_testing_cloud for comprehensive testing

### For Bug Fixes:
1. **Check theme integration**: Ensure all colors use theme variables
2. **Verify responsive behavior**: Test on mobile and desktop
3. **Animation conflicts**: Check App.css for existing animations
4. **Z-index layering**: Navigation should be highest priority (z-50+)

---

## 🎨 Animation System

### Available CSS Animations (App.css):
```css
.animate-fade-in       - Fade in effect
.animate-slide-up      - Slide up from bottom
.animate-scale-in      - Scale in from center
.animate-slide-in-up   - Slide in from bottom (faster)
.animate-slide-in-right - Slide in from right
.animate-bounce-gentle - Gentle bounce effect
.animate-pulse-gentle  - Gentle pulse effect
.animate-float         - Floating animation
.animate-glow          - Glow effect
```

### Framer Motion Integration:
- Used for complex animations and gestures
- Page transitions and component animations
- Mobile menu slide-in/out effects

---

## 📊 Performance Considerations

### Optimization Strategies:
1. **Lazy Loading**: React.lazy() for page components
2. **Code Splitting**: Route-based splitting
3. **Image Optimization**: Responsive images with proper sizing
4. **CSS Optimization**: Tailwind purging unused styles
5. **Bundle Analysis**: Regular bundle size monitoring

### Current Performance Metrics:
- **Initial Load**: < 3s on 3G
- **Interactive**: < 1s after load
- **Mobile Performance**: Optimized for 60fps animations

---

## 🐛 Common Issues & Solutions

### Mobile Navigation Issues:
1. **Overlap Problem**: Use fixed positioning with high z-index
2. **Click-outside**: Implement proper event delegation
3. **Scroll Prevention**: Toggle body overflow when menu open
4. **Animation Lag**: Use transform3d for GPU acceleration

### Theme-related Issues:
1. **Color Inconsistency**: Always use theme variables, never hardcode
2. **Font Loading**: Preload fonts in index.html
3. **Theme Switching**: Clear previous theme classes before applying new ones

### Performance Issues:
1. **Re-renders**: Use React.memo for expensive components
2. **Large Bundles**: Implement code splitting
3. **Animation Jank**: Use will-change CSS property

---

## 🔧 Development Tools & Extensions

### Recommended VS Code Extensions:
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Auto Rename Tag
- Bracket Pair Colorizer
- GitLens

### Browser Dev Tools:
- React Developer Tools
- Redux DevTools (if added)
- Lighthouse for performance auditing

---

## 📈 Project Roadmap

### Phase 1: ✅ Base Implementation
- [x] React app setup with routing
- [x] Theme system implementation
- [x] Basic navigation and pages
- [x] Responsive design foundation

### Phase 2: 🔄 Navigation Enhancement (Current)
- [ ] Premium mobile navigation
- [ ] Enhanced animations and transitions
- [ ] Improved click-outside functionality
- [ ] Advanced visual effects

### Phase 3: 📋 Planned Features
- [ ] User authentication system
- [ ] RSVP form with backend integration
- [ ] Photo gallery with upload functionality
- [ ] Guest book with real-time updates
- [ ] Email notification system

### Phase 4: 🚀 Advanced Features
- [ ] Progressive Web App (PWA)
- [ ] Offline functionality
- [ ] Push notifications
- [ ] Analytics integration
- [ ] Performance optimization

---

## 🤝 Collaboration Guidelines

### For AI Agents:
1. **Read this documentation first** before exploring codebase
2. **Follow established patterns** for consistency
3. **Test thoroughly** before marking tasks complete
4. **Update this documentation** when adding new features
5. **Use existing tooling** rather than introducing new dependencies

### Code Standards:
- **ES6+ JavaScript** with functional components
- **Tailwind CSS** for styling (avoid custom CSS unless necessary)
- **Descriptive naming** for components and functions
- **Comment complex logic** especially animations and state management
- **Mobile-first responsive** design approach

---

## 📞 Emergency Contacts & Resources

### Key Resources:
- **React Documentation**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Framer Motion**: https://www.framer.com/motion/
- **Radix UI**: https://www.radix-ui.com/

### Troubleshooting:
1. **Service Issues**: Check `sudo supervisorctl status`
2. **Build Errors**: Clear node_modules and reinstall
3. **Port Conflicts**: Ensure ports 3000, 8001 are available
4. **Theme Problems**: Verify theme context provider wrapper

---

*Last Updated: January 2025*  
*Status: Mobile Navigation Enhancement in Progress*  
*Next AI Agent: Focus on Navigation.js component enhancement*

---

## 🎯 IMMEDIATE NEXT STEPS FOR AI AGENT

### Current Task: Premium Mobile Navigation Implementation
**File to Modify**: `/app/frontend/src/components/Navigation.js`

#### Requirements:
1. **Full-screen overlay** with blur backdrop (z-index: 9999)
2. **Slide-in animation** from right side
3. **Enhanced click-outside** functionality 
4. **Premium visual effects** - glass morphism, subtle particles
5. **Micro-interactions** - hover effects, smooth transitions
6. **Proper layering** to prevent content overlap

#### Success Criteria:
- [ ] Mobile menu opens with smooth slide-in animation
- [ ] Background content is blurred and non-interactive
- [ ] Clicking outside or on blank areas closes menu
- [ ] Visual design is unique and premium
- [ ] No overlap issues with background content
- [ ] Works across all three themes (classic, modern, boho)

**Implementation Priority**: HIGH - This is the main deliverable