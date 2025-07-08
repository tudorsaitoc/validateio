"""
Supabase client configuration for ValidateIO.

Handles Supabase client initialization and authentication.
"""

from typing import Optional
from supabase import create_client, Client
from gotrue import AuthResponse
from gotrue.errors import AuthError

from app.core.config import settings
from app.core.logging import logger


class SupabaseClient:
    """Wrapper for Supabase client with authentication methods."""
    
    def __init__(self):
        """Initialize Supabase client."""
        if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables"
            )
        
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        
        # Use service key for admin operations if available
        if settings.SUPABASE_SERVICE_KEY:
            self.admin_client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
        else:
            self.admin_client = None
    
    async def sign_up(self, email: str, password: str, user_metadata: dict = None) -> AuthResponse:
        """
        Sign up a new user.
        
        Args:
            email: User's email
            password: User's password
            user_metadata: Additional user metadata
            
        Returns:
            AuthResponse with user and session data
        """
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": user_metadata or {}
                }
            })
            return response
        except AuthError as e:
            logger.error(f"Supabase sign up error: {e}")
            raise
    
    async def sign_in_with_password(self, email: str, password: str) -> AuthResponse:
        """
        Sign in a user with email and password.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            AuthResponse with user and session data
        """
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response
        except AuthError as e:
            logger.error(f"Supabase sign in error: {e}")
            raise
    
    async def sign_out(self) -> None:
        """Sign out the current user."""
        try:
            self.client.auth.sign_out()
        except AuthError as e:
            logger.error(f"Supabase sign out error: {e}")
            raise
    
    async def get_user(self, jwt: str) -> Optional[dict]:
        """
        Get user from JWT token.
        
        Args:
            jwt: JWT token from Authorization header
            
        Returns:
            User data if valid, None otherwise
        """
        try:
            response = self.client.auth.get_user(jwt)
            return response.user if response else None
        except AuthError as e:
            logger.error(f"Supabase get user error: {e}")
            return None
    
    async def refresh_session(self, refresh_token: str) -> AuthResponse:
        """
        Refresh user session with refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            AuthResponse with new session data
        """
        try:
            response = self.client.auth.refresh_session(refresh_token)
            return response
        except AuthError as e:
            logger.error(f"Supabase refresh session error: {e}")
            raise
    
    def get_db(self):
        """Get database client for direct queries."""
        return self.client
    
    def get_admin_db(self):
        """Get admin database client for privileged operations."""
        if not self.admin_client:
            raise ValueError("Admin client not initialized. SUPABASE_SERVICE_KEY required.")
        return self.admin_client


# Global Supabase client instance
supabase_client: Optional[SupabaseClient] = None


def get_supabase() -> SupabaseClient:
    """Get or create Supabase client instance."""
    global supabase_client
    
    if not supabase_client:
        supabase_client = SupabaseClient()
    
    return supabase_client