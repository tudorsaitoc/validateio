from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum

from pydantic import BaseModel, Field


class ValidationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ValidationCreate(BaseModel):
    business_idea: str = Field(..., min_length=10, max_length=1000)
    target_market: Optional[str] = Field(None, max_length=500)
    industry: Optional[str] = Field(None, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_idea": "An AI-powered personal finance app that helps millennials save money",
                "target_market": "Millennials aged 25-35 in urban areas",
                "industry": "FinTech"
            }
        }


class ValidationResponse(BaseModel):
    id: str
    user_id: str
    business_idea: str
    target_market: Optional[str]
    industry: Optional[str]
    status: ValidationStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    # Results
    market_research: Optional[Dict[str, Any]] = None
    experiments: Optional[Dict[str, Any]] = None
    marketing_campaigns: Optional[Dict[str, Any]] = None
    
    # Metrics
    total_cost: Optional[float] = None
    execution_time_seconds: Optional[float] = None
    
    class Config:
        from_attributes = True


class ValidationUpdate(BaseModel):
    status: Optional[ValidationStatus] = None
    market_research: Optional[Dict[str, Any]] = None
    experiments: Optional[Dict[str, Any]] = None
    marketing_campaigns: Optional[Dict[str, Any]] = None
    total_cost: Optional[float] = None
    execution_time_seconds: Optional[float] = None
    completed_at: Optional[datetime] = None


class MarketResearchResult(BaseModel):
    competitors: list[Dict[str, Any]]
    market_size: Dict[str, Any]  # TAM, SAM, SOM
    customer_pain_points: list[str]
    unique_value_proposition: str
    market_trends: list[str]
    confidence_score: float


class ExperimentResult(BaseModel):
    landing_pages: list[Dict[str, Any]]
    ab_tests: list[Dict[str, Any]]
    copy_variations: list[Dict[str, Any]]
    target_audiences: list[Dict[str, Any]]
    predicted_conversion_rate: float


class MarketingCampaignResult(BaseModel):
    ad_campaigns: list[Dict[str, Any]]
    content_strategy: Dict[str, Any]
    channel_recommendations: list[str]
    budget_allocation: Dict[str, float]
    expected_roi: float