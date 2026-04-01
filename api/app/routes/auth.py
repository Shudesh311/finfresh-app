from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from pydantic import BaseModel, validator
from app.database import users
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_token

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Username must be at least 2 characters')
        return v.strip()
    
    @validator('email')
    def validate_email(cls, v):
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v

class LoginRequest(BaseModel):
    login: str
    password: str
    
    @validator('login')
    def validate_login(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Username or email is required')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: RegisterRequest):
    """Register a new user"""
    print(f"📝 Registering: {user.email}")
    
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    try:
        # Check if email exists
        if users.find_one({"email": user.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username exists
        if users.find_one({"name": user.name}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash password
        hashed_password = hash_password(user.password)
        
        # Create user
        user_data = {
            "name": user.name,
            "email": user.email,
            "passwordHash": hashed_password,
            "createdAt": datetime.utcnow()
        }
        
        result = users.insert_one(user_data)
        print(f"✅ User created with ID: {result.inserted_id}")
        
        # Create token
        token = create_token({
            "userId": str(result.inserted_id),
            "email": user.email,
            "name": user.name
        })
        
        return {
            "token": token,
            "user": {
                "id": str(result.inserted_id),
                "name": user.name,
                "email": user.email,
                "createdAt": user_data["createdAt"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/login")
async def login(user: LoginRequest):
    """Login user - accepts username OR email"""
    print(f"🔐 Login attempt with: {user.login}")
    
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    
    try:
        # Find user by email OR username
        db_user = users.find_one({
            "$or": [
                {"email": user.login},
                {"name": user.login}
            ]
        })
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        print(f"✅ Found user: {db_user['email']}")
        
        # Get stored password
        stored_password = db_user.get("passwordHash") or db_user.get("password")
        
        if not stored_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User data corrupted"
            )
        
        # Verify password
        if not verify_password(user.password, stored_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        print(f"✅ Login successful")
        
        # Create token
        token = create_token({
            "userId": str(db_user["_id"]),
            "email": db_user["email"],
            "name": db_user.get("name", "User")
        })
        
        return {
            "token": token,
            "user": {
                "id": str(db_user["_id"]),
                "name": db_user.get("name", "User"),
                "email": db_user["email"],
                "createdAt": db_user.get("createdAt", datetime.utcnow())
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )