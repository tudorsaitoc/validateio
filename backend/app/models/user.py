"""
User model for ValidateIO.

Stores user account information and authentication details.
When using Supabase auth, this model maps to the user_profiles table.
"""

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base
from app.core.config import settings


class User(Base):
    """User model for authentication and account management."""
    
    # Use different table name based on auth mode
    __tablename__ = "user_profiles" if settings.USE_SUPABASE_AUTH else "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # When using Supabase, email is stored in auth.users
    # For custom auth, we store it here
    if not settings.USE_SUPABASE_AUTH:
        email = Column(String, unique=True, nullable=False, index=True)
    
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    
    # Password is handled by Supabase Auth when USE_SUPABASE_AUTH is True
    if not settings.USE_SUPABASE_AUTH:
        hashed_password = Column(String, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    validations = relationship("Validation", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def email(self):
        """Get email from the model or from auth.users when using Supabase."""
        if settings.USE_SUPABASE_AUTH:
            # In Supabase mode, email would be fetched from auth.users
            # This is handled at the API layer
            return None
        return self._email
    
    @email.setter
    def email(self, value):
        """Set email only when not using Supabase auth."""
        if not settings.USE_SUPABASE_AUTH:
            self._email = value