"""
Celery worker configuration for ValidateIO.

Handles async task processing for:
- Market research
- Experiment generation
- Marketing campaign creation
"""

import logging
from celery import Celery
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Celery instance
celery_app = Celery(
    "validateio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"]  # Include task modules
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.AGENT_MAX_EXECUTION_TIME,
    task_soft_time_limit=settings.AGENT_MAX_EXECUTION_TIME - 30,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.validation.run_market_research": {"queue": "research"},
    "app.tasks.validation.run_experiment_generation": {"queue": "experiments"},
    "app.tasks.validation.run_marketing_campaigns": {"queue": "marketing"},
}

logger.info("Celery worker configured successfully")