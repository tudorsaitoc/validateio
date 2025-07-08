"""
Validation model for ValidateIO.

Stores business idea validation requests and results.
"""

from sqlalchemy import Column, String, Text, Float, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
import enum

from app.db.base import Base


class ValidationStatus(str, enum.Enum):
    """Validation status enum."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Validation(Base):
    """Model for business idea validation requests."""
    
    __tablename__ = "validations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Request data
    business_idea = Column(Text, nullable=False)
    target_market = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    
    # Processing
    status = Column(Enum(ValidationStatus), default=ValidationStatus.PENDING, nullable=False)
    task_id = Column(String, nullable=True)  # Celery task ID
    
    # Results
    market_research = Column(JSONB, nullable=True)
    experiments = Column(JSONB, nullable=True)
    marketing_campaigns = Column(JSONB, nullable=True)
    
    # Metrics
    total_cost = Column(Float, nullable=True)
    execution_time_seconds = Column(Float, nullable=True)
    
    # Timestamps
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="validations")