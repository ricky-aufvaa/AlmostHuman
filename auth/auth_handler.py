from jose import jwt
from datetime import datetime, timedelta
import bcrypt
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AuthHandler:
    def __init__(self):
        # Use a secret key from environment or default
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password using bcrypt"""
        # Ensure password is a string and strip any whitespace
        password = str(password).strip()
        
        # Encode password to bytes
        password_bytes = password.encode('utf-8')
        
        # Truncate to 72 bytes if necessary (bcrypt limitation)
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Generate salt and hash
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash using bcrypt"""
        # Ensure password is a string and strip any whitespace
        plain_password = str(plain_password).strip()
        
        # Encode password to bytes
        password_bytes = plain_password.encode('utf-8')
        
        # Truncate to 72 bytes if necessary (bcrypt limitation)
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Encode hashed password to bytes if it's a string
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        
        # Verify password
        return bcrypt.checkpw(password_bytes, hashed_password)
    
    def encode_token(self, user_id: int) -> str:
        """Create a JWT token"""
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> Optional[int]:
        """Decode a JWT token and return user_id"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("user_id")
            return user_id
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh an existing token"""
        user_id = self.decode_token(token)
        if user_id:
            return self.encode_token(user_id)
        return None
