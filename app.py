from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import auth and database modules
from auth.auth_handler import AuthHandler
from auth.models import User, UserCreate, UserLogin, Token
from auth.database import get_db, create_tables
from sqlalchemy.orm import Session

# Import RAG system
import sys
sys.path.append('./RAG')
from RAG.chains import chain_with_message_history

app = FastAPI(title="RAG System with Authentication", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize auth handler
auth_handler = AuthHandler()
security = HTTPBearer()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Pydantic models for requests
class QueryRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default_session"

class QueryResponse(BaseModel):
    answer: str
    session_id: str

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = auth_handler.decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Auth endpoints
@app.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists by email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    try:
        # Create new user
        hashed_password = auth_handler.get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Generate token
        access_token = auth_handler.encode_token(new_user.id)
        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )

@app.post("/signin", response_model=Token)
async def signin(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not auth_handler.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Generate token
    access_token = auth_handler.encode_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Alias for signin endpoint"""
    return await signin(user_credentials, db)

# Protected RAG endpoint
@app.post("/query", response_model=QueryResponse)
async def query_rag(
    query_request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        # Use user-specific session ID
        session_id = f"{current_user.id}_{query_request.session_id}"
        
        response = chain_with_message_history.invoke(
            {"question": query_request.question},
            config={"configurable": {"session_id": session_id}},
        )
        
        return QueryResponse(
            answer=response,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )

# User profile endpoint
@app.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "created_at": current_user.created_at
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
