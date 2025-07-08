import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.schemas.user import User, UserUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user(
    current_user: User = Depends(deps.get_current_user),
) -> User:
    """
    Get current user profile.
    """
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    *,
    user_update: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> User:
    """
    Update current user profile.
    """
    # TODO: Implement user update in database
    
    # For now, return the current user with updates applied
    user_data = current_user.model_dump()
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            user_data[field] = value
    
    updated_user = User(**user_data)
    return updated_user


@router.delete("/me")
async def delete_current_user(
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Delete current user account.
    """
    # TODO: Implement user deletion
    return {"message": "User account deleted successfully"}