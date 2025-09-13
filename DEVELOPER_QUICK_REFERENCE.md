# ⚡ **DEVELOPER QUICK REFERENCE GUIDE**
### *Essential Information for New Developers - Wedding Card Project v2.3*
### *Updated: September 13, 2025 - MongoDB Integration & Personalization Fix Complete*

---

## 🚀 **GET STARTED IN 5 MINUTES**

### **1. Environment Status** ✅
```bash
# Everything already set up and working
cd /app

# Services running
sudo supervisorctl status
# frontend    RUNNING ✅
# backend     RUNNING ✅  
# mongodb     RUNNING ✅ (Atlas)

# Quick test
curl http://localhost:8001/api/test
# {"status":"ok","message":"Backend is working"}
```

### **2. Access Points** ✅
- **Frontend**: http://localhost:3000 ✅
- **Backend**: http://localhost:8001 ✅
- **API Docs**: http://localhost:8001/docs ✅
- **MongoDB**: Atlas cloud database ✅

### **3. Test Complete User Flow** ✅
```bash
# 1. Public URL with personalization (WORKING)
curl http://localhost:8001/api/wedding/public/custom/sridharandsneha
# Returns: Sridhar & Sneha personalized data ✅

# 2. Frontend public URL (WORKING)
# Visit: http://localhost:3000/sridharandsneha
# Shows: "Sridhar & Sneha" + personalized content ✅

# 3. Dashboard functionality (WORKING)
# Click floating button → Register → Dashboard → Edit features ✅
```

---

## 🚨 **CRITICAL UPDATE: Major Issue RESOLVED**

### **✅ PERSONALIZATION FIX COMPLETE**
- **Problem**: Public URLs showed default data instead of personalized data
- **Solution**: MongoDB integration with backend API data fetching
- **Status**: ✅ COMPLETELY RESOLVED
- **Verification**: `/sridharandsneha` correctly shows "Sridhar & Sneha" content

### **Before You Start**
**DO NOT REBUILD** these components - they're working perfectly:
- ✅ MongoDB Atlas integration
- ✅ Public URL personalization system
- ✅ Backend API endpoints
- ✅ Frontend data fetching
- ✅ User authentication
- ✅ Navigation and theming

---

## 📋 **PROJECT ARCHITECTURE - 30 SECOND OVERVIEW**

```
┌─ React Frontend (Port 3000) ────────────────────┐
│  ├─ 🌐 PUBLIC URL SYSTEM ✅ WORKING              │
│  │   ├─ Custom URLs (e.g., /sridharandsneha)    │
│  │   └─ PersonalizedPage fetches from API       │
│  ├─ 🎛️ DASHBOARD ✅ WORKING                      │
│  │   ├─ User registration and editing            │
│  │   ├─ Custom URL generation                    │
│  │   └─ QR code and sharing features             │
│  ├─ 📱 Mobile Responsive ✅ WORKING               │
│  └─ 🎨 Three Themes ✅ WORKING                    │
└─────────────────────────────────────────────────┘
           │
           ▼ REST API calls
┌─ FastAPI Backend (Port 8001) ──────────────────┐
│  ├─ 🍃 MongoDB Atlas ✅ CONNECTED               │
│  │   ├─ users collection (authentication)       │
│  │   └─ weddings collection (personalized data) │
│  ├─ 📂 JSON Fallback ✅ CONFIGURED               │
│  ├─ 🔗 Public APIs ✅ WORKING                    │
│  │   └─ /api/wedding/public/custom/{url}        │
│  └─ 🔄 Auto-serialization ✅ WORKING             │
└─────────────────────────────────────────────────┘
```

---

## 🔧 **CRITICAL FILES - PRIORITY READING**

### **🟥 MUST UNDERSTAND (Recently Updated)**
| File | Purpose | Status | Priority |
|------|---------|---------|----------|
| `/backend/server.py` | **🍃 MongoDB integration & APIs** | ✅ WORKING | 🔴 CRITICAL |
| `/frontend/src/pages/PublicWeddingPage.js` | **🌐 Public URL personalization** | ✅ FIXED | 🔴 CRITICAL |
| `/backend/.env` | **🔑 MongoDB Atlas connection** | ✅ CONFIGURED | 🔴 CRITICAL |
| `/frontend/src/contexts/UserDataContext.js` | **💾 Data management** | ✅ WORKING | 🟡 HIGH |

### **🟡 IMPORTANT (Stable - No Changes Needed)**
| File | Purpose | Status | Priority |
|------|---------|---------|----------|
| `/frontend/src/components/LeftSidebar.js` | Enhanced dashboard sidebar | ✅ WORKING | 🟡 HIGH |
| `/frontend/src/pages/LoginPage.js` | LocalStorage authentication | ✅ WORKING | 🟡 HIGH |
| `/frontend/src/App.js` | Routing & custom URLs | ✅ WORKING | 🟡 HIGH |

### **🟢 REFERENCE (When Adding Features)**
| File | Purpose | Status | Priority |
|------|---------|---------|----------|
| `/frontend/src/App.css` | Premium animations & styles | ✅ WORKING | 🟢 MEDIUM |
| All page components | Individual page functionality | ✅ WORKING | 🟢 LOW |

---

## 🍃 **MONGODB INTEGRATION - MEMORIZE THIS**

### **Connection Details** ✅
```javascript
// Already configured in /backend/.env
MONGO_URL="mongodb+srv://prasannagoudasp12_db_user:RVj1n8gEkHewSwIL@cluster0.euowph1.mongodb.net/..."
DB_NAME="weddingcard"

// Collections:
// - users: User authentication data
// - weddings: Wedding data with custom URLs for public access
```

### **Key API Endpoints** ✅
```javascript
// Public access (WORKING - don't rebuild)
GET /api/wedding/public/custom/{custom_url}  // Gets personalized data
GET /api/wedding/public/user/{user_id}       // Alternative access
GET /api/wedding/public/{wedding_id}         // Direct access

// Private access (WORKING)
POST /api/wedding                            // Create wedding data
PUT /api/wedding                             // Update wedding data  
GET /api/wedding?session_id={id}             // Get user's data

// Authentication (WORKING)
POST /api/auth/register                      // User registration
POST /api/auth/login                         // User login
```

### **Data Structure** ✅
```javascript
// Wedding data in MongoDB (don't change structure)
{
  "id": "uuid-string",
  "user_id": "uuid-string", 
  "couple_name_1": "Sridhar",
  "couple_name_2": "Sneha",
  "wedding_date": "2025-06-15",
  "venue_name": "Garden Paradise Resort",
  "venue_location": "Garden Paradise Resort • Bangalore, India",
  "their_story": "We met during college days...",
  "custom_url": "sridharandsneha",  // For public access
  "theme": "classic",
  "story_timeline": [...],
  "schedule_events": [...],
  // ... other fields
}
```

---

## 🎯 **PERSONALIZATION SYSTEM - UNDERSTAND THIS**

### **How Public URLs Work** ✅
```
1. User registers and creates wedding data in dashboard
   ↓
2. Data saved to MongoDB with custom_url field (e.g., "sridharandsneha")
   ↓  
3. User shares custom URL: /sridharandsneha
   ↓
4. Visitor accesses URL → PublicWeddingPage component loads
   ↓
5. Component calls API: /api/wedding/public/custom/sridharandsneha
   ↓
6. Backend queries MongoDB for wedding with custom_url="sridharandsneha"
   ↓
7. Returns personalized data: Sridhar & Sneha, Garden Paradise Resort, etc.
   ↓
8. Frontend displays full wedding website with personalized content
```

### **Testing Personalization** ✅
```bash
# API test (should return personalized data)
curl http://localhost:8001/api/wedding/public/custom/sridharandsneha

# Frontend test (should show personalized content)
# Visit: http://localhost:3000/sridharandsneha
# Should show: "Sridhar & Sneha" NOT "Sarah & Michael"
```

---

## 🛠️ **COMMON DEVELOPMENT TASKS**

### **Adding New Wedding Data Fields**
```javascript
// 1. Add field to MongoDB wedding data structure (in API)
// 2. Update PublicWeddingPage to display the new field
// 3. Add editing form in LeftSidebar.js dashboard
// 4. Test that public URLs show the new field correctly

// Example: Adding phone number field
// Backend: Add "phone_number" to wedding data model
// Frontend: Display phone in PublicWeddingPage
// Dashboard: Add phone input in appropriate form section
// Test: Verify /sridharandsneha shows the phone number
```

### **Adding New Form Section** 
```javascript
// Follow existing patterns in LeftSidebar.js
// 1. Add to editSections array
{ id: 'new_section', label: 'New Section', icon: IconName, description: 'Description' }

// 2. Add form in FormPopup renderForm() switch statement  
case 'new_section':
  return <NewSectionForm />

// 3. Ensure PublicWeddingPage displays the new section data
// 4. Test on public URLs
```

### **Testing New Features**
```bash
# Always test these when adding features:
# 1. Backend API response
curl http://localhost:8001/api/wedding/public/custom/sridharandsneha

# 2. Frontend public URL display
# Visit: http://localhost:3000/sridharandsneha  

# 3. Dashboard editing 
# Register → Login → Edit new section → Save

# 4. Mobile responsiveness
# Test on mobile devices

# 5. All three themes
# Test Classic, Modern, Boho themes
```

---

## 🚨 **CRITICAL RULES - NEVER BREAK THESE**

### **MongoDB Rules**
```javascript
// ❌ WRONG - Don't query localStorage for public URLs
const data = localStorage.getItem('wedding_data');

// ✅ CORRECT - Always use MongoDB API for public access
const response = await fetch(`/api/wedding/public/custom/${customUrl}`);
const data = await response.json();
```

### **Public URL Rules**
```javascript
// ❌ WRONG - Hardcoding data or using localStorage
const weddingData = { couple_name_1: "Sarah", couple_name_2: "Michael" };

// ✅ CORRECT - Fetch personalized data from API
useEffect(() => {
  const fetchData = async () => {
    const response = await fetch(`${backendUrl}/api/wedding/public/custom/${customUrl}`);
    const personalizedData = await response.json();
    setWeddingData(personalizedData);
  };
  fetchData();
}, [customUrl]);
```

### **Component Integration Rules**
```javascript
// ❌ WRONG - Not considering public URL context
const { weddingData } = useUserData(); // Only works for logged-in users

// ✅ CORRECT - Handle both dashboard and public URL contexts
const { weddingData } = useUserData(); // For dashboard
const [publicData, setPublicData] = useState(null); // For public URLs
const finalData = publicData || weddingData; // Use appropriate data source
```

---

## 🔍 **DEBUGGING QUICK COMMANDS**

### **Check System Status**
```bash
# Services status
sudo supervisorctl status

# Backend API test
curl http://localhost:8001/api/test

# MongoDB connection test (check backend logs)
tail -f /var/log/supervisor/backend.out.log

# Frontend build status
cd /app/frontend && yarn build
```

### **Debug Public URL Issues**
```bash
# 1. Test API directly
curl http://localhost:8001/api/wedding/public/custom/sridharandsneha

# 2. Check backend logs
tail -f /var/log/supervisor/backend.out.log

# 3. Check frontend console (browser DevTools)
# Look for: "Found wedding data by custom URL" message

# 4. Verify MongoDB data
# API should return personalized data, not default
```

### **Reset Development Environment**
```bash
# If something is broken, restart services
sudo supervisorctl restart all

# Check all services are running
sudo supervisorctl status

# Test critical functionality
curl http://localhost:8001/api/wedding/public/custom/sridharandsneha
```

---

## 📊 **CURRENT PROJECT STATUS**

### **✅ WORKING PERFECTLY (Don't Touch)**
- MongoDB Atlas connection and data persistence
- Public URL personalization (`/sridharandsneha` shows Sridhar & Sneha)
- Backend API endpoints (all tested and working)
- Frontend data fetching and display
- User authentication and session management
- Dashboard editing functionality
- Navigation and theme systems
- Mobile responsive design

### **🔄 NEEDS DEVELOPMENT (Your Focus)**
- **RSVP Section**: Guest management and response tracking
- **Gallery Section**: Photo upload and organization system
- **Wedding Party Section**: Bridal/groom party member management
- **Registry Section**: Gift registry and honeymoon fund management
- **Guest Book Section**: Message management and moderation
- **FAQ Section**: Question and answer management system

### **🔍 DEVELOPMENT APPROACH**
1. **Study existing patterns** in working sections (Home, Story, Schedule)
2. **Follow MongoDB integration** - store data in database, fetch via API
3. **Test public URLs** - ensure new features work on `/sridharandsneha`
4. **Maintain responsiveness** - test on mobile and desktop
5. **Support all themes** - verify Classic, Modern, Boho themes work

---

## 📚 **DOCUMENTATION HIERARCHY**

### **Read in This Order**
1. **This file** - Quick start and current status
2. **COMPLETE_PROJECT_DOCUMENTATION.md** - Comprehensive technical details
3. **TESTING_STATUS_REPORT.md** - What's tested and verified working
4. **PROJECT_DOCUMENTATION.md** - Original architecture and setup
5. **MOBILE_NAVIGATION_IMPLEMENTATION_SUMMARY.md** - Mobile-specific details

---

## 🎯 **IMMEDIATE ACTION ITEMS FOR NEW DEVS**

### **Day 1 - Understand What's Working** ✅
- [ ] Test public URL personalization: http://localhost:3000/sridharandsneha
- [ ] Verify API responses: `curl http://localhost:8001/api/wedding/public/custom/sridharandsneha`
- [ ] Explore dashboard functionality: Register → Login → Edit wedding data
- [ ] Check MongoDB data structure and connection
- [ ] Review existing form sections (Home, Story, Schedule) as examples

### **Day 2 - Plan Feature Development**
- [ ] Choose which form section to implement first (RSVP recommended)
- [ ] Study existing form patterns in LeftSidebar.js
- [ ] Understand data flow: Dashboard → MongoDB → Public URL
- [ ] Plan API endpoints needed for your chosen section
- [ ] Design form UI following existing patterns

### **Day 3 - Start Implementation**
- [ ] Add new section to editSections array in LeftSidebar.js
- [ ] Create form component following existing patterns
- [ ] Add backend API endpoints if needed
- [ ] Test data storage in MongoDB
- [ ] Verify public URLs display new section data

---

## 🚨 **GOTCHAS & COMMON MISTAKES**

### **MongoDB Gotchas**
- **Document Structure**: Don't change existing field names (couple_name_1, couple_name_2, etc.)
- **Custom URLs**: Always test that new data appears on public URLs like `/sridharandsneha`
- **ObjectId Handling**: Use existing serialization - don't modify serialize_mongo_doc()
- **Connection Issues**: Backend automatically falls back to JSON files if MongoDB unavailable

### **Public URL Gotchas**
- **Data Source**: Public URLs use API calls, not localStorage
- **Route Matching**: Custom URLs are catch-all routes - test carefully
- **Theme Application**: Ensure themes work correctly on public URLs
- **Navigation**: All nav links should work on public URLs

### **Development Gotchas**
- **Don't Rebuild**: Core system is working - extend, don't replace
- **Test Personalization**: Always verify your changes work on `/sridharandsneha`
- **Mobile Testing**: Test responsive design for any new components
- **Theme Consistency**: New features should work with all three themes

---

## 🎉 **SUCCESS METRICS**

### **You've Mastered This When You Can:**
- [ ] Explain how public URL personalization works (MongoDB → API → Frontend)
- [ ] Add a new form section that shows up on public URLs
- [ ] Debug API issues using curl and backend logs
- [ ] Test new features across mobile, desktop, and all themes
- [ ] Understand the difference between dashboard data and public URL data
- [ ] Follow existing code patterns without breaking working functionality

---

## 📞 **GETTING HELP**

### **Error Resolution Priority**
1. **Check API responses** with curl before debugging frontend
2. **Verify MongoDB connection** in backend logs
3. **Test public URLs** after any wedding data changes
4. **Check browser console** for frontend errors
5. **Review existing patterns** in working components

### **Documentation References**
- **FastAPI**: https://fastapi.tiangolo.com/
- **MongoDB**: https://docs.mongodb.com/
- **Motor Driver**: https://motor.readthedocs.io/
- **React**: https://react.dev/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## 🎯 **FINAL WORDS**

This project has **solid foundations** with:
- ✅ **MongoDB integration working**
- ✅ **Public URL personalization working**  
- ✅ **API endpoints tested and documented**
- ✅ **Frontend components rendering correctly**
- ✅ **Mobile responsiveness verified**
- ✅ **All three themes functional**

**Your job**: Build upon this working foundation. Don't reinvent what's already working perfectly - extend it with the remaining form sections.

**Remember**: The hard part (personalization fix) is done. Now it's about following established patterns to add the remaining features.

---

*Quick Reference Version: 2.3*  
*Last Updated: September 13, 2025*  
*Status: ✅ PRODUCTION READY - Core functionality complete*  
*Target Audience: New developers extending the application*