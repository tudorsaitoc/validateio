import logging
from typing import Optional, Dict, Any
from celery.result import AsyncResult

from app.tasks.validation import run_full_validation
from app.core.config import settings

logger = logging.getLogger(__name__)


class ValidationService:
    """Service for handling business idea validations."""
    
    @staticmethod
    async def process_validation(
        validation_id: str,
        user_id: str,
        business_idea: str,
        target_market: Optional[str] = None,
        industry: Optional[str] = None,
    ) -> str:
        """
        Process a validation request asynchronously using Celery.
        
        This method orchestrates the three main validation agents:
        1. Market Research Agent
        2. Experiment Generator Agent
        3. Marketing Autopilot Agent
        
        Args:
            validation_id: Unique validation ID
            user_id: User who requested the validation
            business_idea: The business idea to validate
            target_market: Optional target market specification
            industry: Optional industry specification
            
        Returns:
            Celery task ID for tracking
        """
        logger.info(f"Starting validation process for {validation_id}")
        
        # Queue the validation workflow
        task = run_full_validation.delay(
            validation_id=validation_id,
            business_idea=business_idea,
            target_market=target_market,
            industry=industry
        )
        
        # TODO: Update validation record in database with task_id
        # await update_validation_task_id(validation_id, task.id)
        
        logger.info(f"Validation {validation_id} queued with task ID: {task.id}")
        
        return task.id
    
    @staticmethod
    async def get_validation_status(
        validation_id: str,
        task_id: str
    ) -> Dict[str, Any]:
        """
        Get the current status of a validation task.
        
        Args:
            validation_id: The validation ID
            task_id: The Celery task ID
            
        Returns:
            Status information including progress and current step
        """
        result = AsyncResult(task_id)
        
        status_map = {
            "PENDING": "pending",
            "STARTED": "processing",
            "SUCCESS": "completed",
            "FAILURE": "failed",
            "RETRY": "processing",
            "REVOKED": "cancelled"
        }
        
        status = status_map.get(result.state, "unknown")
        
        # Get progress information
        info = result.info or {}
        progress = 0
        current_step = "Initializing validation"
        
        if status == "processing" and isinstance(info, dict):
            # Extract progress from task info
            if "current" in info and "total" in info:
                progress = int((info["current"] / info["total"]) * 100)
            current_step = info.get("description", "Processing validation")
        elif status == "completed":
            progress = 100
            current_step = "Validation complete"
        elif status == "failed":
            current_step = f"Validation failed: {info}"
        
        return {
            "validation_id": validation_id,
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "current_step": current_step,
            "result": result.result if status == "completed" else None
        }
    
    @staticmethod
    async def cancel_validation(task_id: str) -> bool:
        """
        Cancel a running validation task.
        
        Args:
            task_id: The Celery task ID
            
        Returns:
            True if cancelled successfully
        """
        try:
            result = AsyncResult(task_id)
            result.revoke(terminate=True)
            logger.info(f"Cancelled validation task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel validation task {task_id}: {e}")
            return False