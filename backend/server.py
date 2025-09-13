from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# JSON file for simple user storage
USERS_FILE = ROOT_DIR / 'users.json'
WEDDINGS_FILE = ROOT_DIR / 'weddings.json'

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Simple session storage (in production, use Redis or similar)
active_sessions = {}

# Models
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str  # Simple plain text password
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WeddingData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    couple_name_1: str
    couple_name_2: str
    wedding_date: str
    venue_name: str
    venue_location: str
    their_story: str
    schedule_events: List[dict] = []
    gallery_photos: List[str] = []
    bridal_party: List[dict] = []
    groom_party: List[dict] = []
    faqs: List[dict] = []
    theme: str = "classic"
    custom_url: Optional[str] = ""
    story_timeline: List[dict] = []
    registry_items: List[dict] = []
    honeymoon_fund: Optional[dict] = None
    important_info: Optional[dict] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WeddingDataCreate(BaseModel):
    couple_name_1: str
    couple_name_2: str
    wedding_date: str
    venue_name: str
    venue_location: str
    their_story: str
    schedule_events: List[dict] = []
    gallery_photos: List[str] = []
    bridal_party: List[dict] = []
    groom_party: List[dict] = []
    faqs: List[dict] = []
    theme: str = "classic"

class AuthResponse(BaseModel):
    session_id: str
    user_id: str
    username: str
    success: bool

# Simple file operations
def load_json_file(filename):
    if not filename.exists():
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)

# Simple authentication helper functions
def create_simple_session(user_id: str) -> str:
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = {
        "user_id": user_id,
        "created_at": datetime.utcnow()
    }
    return session_id

def get_current_user_simple(session_id: str = None):
    if not session_id or session_id not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    
    session = active_sessions[session_id]
    users = load_json_file(USERS_FILE)
    
    user_data = None
    for user_id, user_info in users.items():
        if user_id == session["user_id"]:
            user_data = user_info
            break
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return User(**user_data)

# Auth Routes - Simple String Comparison
@api_router.post("/auth/register", response_model=AuthResponse)
async def register(user_data: UserRegister):
    users = load_json_file(USERS_FILE)
    
    # Check if user already exists (simple string comparison)
    for user_id, user_info in users.items():
        if user_info["username"] == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
    
    # Create new user with plain text password
    user = User(
        username=user_data.username,
        password=user_data.password  # Store plain text password (naive approach)
    )
    
    # Save to JSON file
    users[user.id] = user.dict()
    save_json_file(USERS_FILE, users)
    
    # Create simple session
    session_id = create_simple_session(user.id)
    
    return AuthResponse(
        session_id=session_id,
        user_id=user.id,
        username=user.username,
        success=True
    )

@api_router.post("/auth/login", response_model=AuthResponse)
async def login(user_data: UserLogin):
    users = load_json_file(USERS_FILE)
    
    # Simple string comparison authentication
    for user_id, user_info in users.items():
        if (user_info["username"] == user_data.username and 
            user_info["password"] == user_data.password):  # Plain text comparison
            
            # Create simple session
            session_id = create_simple_session(user_id)
            
            return AuthResponse(
                session_id=session_id,
                user_id=user_id,
                username=user_info["username"],
                success=True
            )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

# Simple Wedding Data Routes using JSON files
@api_router.post("/wedding")
async def create_wedding_data(request_data: dict):
    session_id = request_data.get('session_id')
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID required"
        )
    
    current_user = get_current_user_simple(session_id)
    weddings = load_json_file(WEDDINGS_FILE)
    
    # Check if user already has wedding data
    for wedding_id, wedding_info in weddings.items():
        if wedding_info.get("user_id") == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has a wedding card. Use update endpoint instead."
            )
    
    # Remove session_id from the data before creating wedding
    wedding_create_data = {k: v for k, v in request_data.items() if k != 'session_id'}
    
    wedding = WeddingData(
        user_id=current_user.id,
        **wedding_create_data
    )
    
    weddings[wedding.id] = wedding.dict()
    save_json_file(WEDDINGS_FILE, weddings)
    return wedding.dict()

@api_router.put("/wedding")
async def update_wedding_data(request_data: dict):
    session_id = request_data.get('session_id')
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID required"
        )
    
    current_user = get_current_user_simple(session_id)
    weddings = load_json_file(WEDDINGS_FILE)
    
    # Find existing wedding
    existing_wedding_id = None
    for wedding_id, wedding_info in weddings.items():
        if wedding_info.get("user_id") == current_user.id:
            existing_wedding_id = wedding_id
            break
    
    if not existing_wedding_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding data not found"
        )
    
    # Remove session_id from the data before updating
    updated_data = {k: v for k, v in request_data.items() if k != 'session_id'}
    updated_data["updated_at"] = datetime.utcnow()
    updated_data["user_id"] = current_user.id
    updated_data["id"] = existing_wedding_id
    
    weddings[existing_wedding_id] = updated_data
    save_json_file(WEDDINGS_FILE, weddings)
    
    return updated_data

@api_router.get("/wedding")
async def get_wedding_data(session_id: str):
    current_user = get_current_user_simple(session_id)
    weddings = load_json_file(WEDDINGS_FILE)
    
    for wedding_id, wedding_info in weddings.items():
        if wedding_info.get("user_id") == current_user.id:
            return wedding_info
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wedding data not found"
    )

@api_router.get("/wedding/public/{wedding_id}")
async def get_public_wedding_data(wedding_id: str):
    weddings = load_json_file(WEDDINGS_FILE)
    
    if wedding_id not in weddings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding not found"
        )
    
    wedding = weddings[wedding_id]
    # Remove sensitive data for public access
    public_data = {k: v for k, v in wedding.items() if k not in ["user_id"]}
    return public_data

@api_router.get("/wedding/public/custom/{custom_url}")
async def get_public_wedding_by_custom_url(custom_url: str):
    weddings = load_json_file(WEDDINGS_FILE)
    
    # Search for wedding data by custom URL
    for wedding_id, wedding_info in weddings.items():
        if wedding_info.get("custom_url") == custom_url:
            # Remove sensitive data for public access
            public_data = {k: v for k, v in wedding_info.items() if k not in ["user_id"]}
            return public_data
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wedding not found with this custom URL"
    )

@api_router.get("/wedding/public/user/{user_id}")
async def get_public_wedding_by_user_id(user_id: str):
    weddings = load_json_file(WEDDINGS_FILE)
    
    # Search for wedding data by user ID
    for wedding_id, wedding_info in weddings.items():
        if wedding_info.get("user_id") == user_id:
            # Remove sensitive data for public access
            public_data = {k: v for k, v in wedding_info.items() if k not in ["user_id"]}
            return public_data
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Wedding not found for this user"
    )

# Get user profile - Simple version
@api_router.get("/profile")
async def get_profile(session_id: str):
    current_user = get_current_user_simple(session_id)
    return {
        "id": current_user.id,
        "username": current_user.username,
        "created_at": current_user.created_at
    }

# Test endpoint to verify connectivity
@api_router.get("/test")
async def test_endpoint():
    return {"status": "ok", "message": "Backend is working", "timestamp": datetime.utcnow()}

# Legacy routes for compatibility
@api_router.get("/")
async def root():
    return {"message": "Wedding Cards API", "status": "running"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Simple cleanup on shutdown
@app.on_event("shutdown")
async def cleanup():
    active_sessions.clear()