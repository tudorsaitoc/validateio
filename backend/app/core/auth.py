"""
Authentication module for ValidateIO.

Supports both custom JWT and Supabase authentication based on configuration.
"""

from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.logging import logger
from app.core.supabase import get_supabase
from app.models.user import User
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthHandler:
    """Handles authentication logic for both custom JWT and Supabase."""
    
    def __init__(self):
        self.use_supabase = settings.USE_SUPABASE_AUTH
        if self.use_supabase:
            self.supabase = get_supabase()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token (for custom auth)."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:
        """Create JWT refresh token (for custom auth)."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    async def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token (supports both custom and Supabase tokens)."""
        if self.use_supabase:
            # Verify Supabase token
            user = await self.supabase.get_user(token)
            return user
        else:
            # Verify custom JWT token
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                return payload
            except JWTError:
                return None
    
    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        """Get current authenticated user."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        token = credentials.credentials
        
        if self.use_supabase:
            # Get user from Supabase
            user_data = await self.supabase.get_user(token)
            if not user_data:
                raise credentials_exception
            
            # Get user from database using Supabase user ID
            result = await db.execute(
                select(User).where(User.id == user_data.get("id"))
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise credentials_exception
        else:
            # Get user from custom JWT
            payload = await self.verify_token(token)
            if not payload:
                raise credentials_exception
            
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            
            # Get user from database
            result = await db.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                raise credentials_exception
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return user
    
    async def get_current_active_user(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current active user."""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    async def get_current_superuser(
        self,
        current_user: User = Depends(get_current_user)
    ) -> User:
        """Get current superuser."""
        if not current_user.is_superuser:
            raise HTTPException(
                status_code=403,
                detail="The user doesn't have enough privileges"
            )
        return current_user


# Create global auth handler instance
auth_handler = AuthHandler()


# Export commonly used dependencies
get_current_user = auth_handler.get_current_user
get_current_active_user = auth_handler.get_current_active_user
get_current_superuser = auth_handler.get_current_superuser