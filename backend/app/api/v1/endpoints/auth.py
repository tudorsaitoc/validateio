import logging
from datetime import datetime, timedelta
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.auth import auth_handler
from app.core.supabase import get_supabase
from app.schemas.auth import Token, LoginRequest
from app.schemas.user import User, UserCreate
from app.models.user import User as UserModel
from app.db.session import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=User)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Register a new user.
    """
    if settings.USE_SUPABASE_AUTH:
        # Use Supabase authentication
        supabase = get_supabase()
        
        try:
            # Create user in Supabase Auth
            auth_response = await supabase.sign_up(
                email=user_in.email,
                password=user_in.password,
                user_metadata={
                    "full_name": user_in.full_name,
                    "username": user_in.email.split("@")[0]  # Default username
                }
            )
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create user"
                )
            
            # User profile is automatically created by database trigger
            # Just return the user data
            return User(
                id=auth_response.user.id,
                email=auth_response.user.email,
                full_name=user_in.full_name,
                is_active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    else:
        # Use custom authentication
        # Check if user exists
        result = await db.execute(
            select(UserModel).where(UserModel.email == user_in.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and create user
        user = UserModel(
            id=uuid.uuid4(),
            email=user_in.email,
            username=user_in.email.split("@")[0],
            full_name=user_in.full_name,
            hashed_password=auth_handler.get_password_hash(user_in.password),
            is_active=True,
            is_verified=False,
            is_superuser=False,
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return User(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    if settings.USE_SUPABASE_AUTH:
        # Use Supabase authentication
        supabase = get_supabase()
        
        try:
            # Sign in with Supabase
            auth_response = await supabase.sign_in_with_password(
                email=form_data.username,
                password=form_data.password
            )
            
            if not auth_response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            return Token(
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token,
                token_type="bearer",
            )
            
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    else:
        # Use custom authentication
        # Get user from database
        result = await db.execute(
            select(UserModel).where(UserModel.email == form_data.username)
        )
        user = result.scalar_one_or_none()
        
        if not user or not auth_handler.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires,
        )
        refresh_token = auth_handler.create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str) -> Token:
    """
    Refresh access token using refresh token.
    """
    if settings.USE_SUPABASE_AUTH:
        # Use Supabase refresh
        supabase = get_supabase()
        
        try:
            auth_response = await supabase.refresh_session(refresh_token)
            
            if not auth_response.session:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            return Token(
                access_token=auth_response.session.access_token,
                refresh_token=auth_response.session.refresh_token,
                token_type="bearer",
            )
            
        except Exception as e:
            logger.error(f"Refresh token error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    else:
        # Use custom JWT refresh
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")
            
            if user_id is None or token_type != "refresh":
                raise credentials_exception
                
        except JWTError:
            raise credentials_exception
        
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_handler.create_access_token(
            data={"sub": user_id, "email": payload.get("email")},
            expires_delta=access_token_expires,
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
        )