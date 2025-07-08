"""
Celery tasks for validation processing.

These tasks handle the async execution of:
- Market research
- Experiment generation  
- Marketing campaign creation
"""

import asyncio
import logging
import time
from typing import Any, Dict
from celery import Task
from app.worker import celery_app
from app.agents import MarketResearchAgent, ExperimentGeneratorAgent, MarketingAutopilotAgent
from app.core.config import settings

logger = logging.getLogger(__name__)


class ValidationTask(Task):
    """Base task with error handling and cost tracking."""
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure."""
        logger.error(f"Task {task_id} failed: {exc}")
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Handle task retry."""
        logger.warning(f"Task {task_id} retrying: {exc}")


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_market_research",
    max_retries=settings.AGENT_MAX_RETRIES,
    default_retry_delay=60,
)
def run_market_research(
    self,
    validation_id: str,
    business_idea: str,
    target_market: str = None,
    industry: str = None,
) -> Dict[str, Any]:
    """
    Run market research for a business idea.
    
    Args:
        validation_id: The validation request ID
        business_idea: The business idea to research
        target_market: Optional target market
        industry: Optional industry
        
    Returns:
        Market research results
    """
    try:
        logger.info(f"Starting market research for validation {validation_id}")
        start_time = time.time()
        
        # Initialize and run the market research agent
        agent = MarketResearchAgent()
        
        # Run async method in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(
                agent.research(
                    business_idea=business_idea,
                    target_market=target_market,
                    industry=industry
                )
            )
        finally:
            loop.close()
        
        execution_time = time.time() - start_time
        logger.info(f"Market research completed in {execution_time:.2f} seconds")
        
        # Add metadata
        results["execution_time_seconds"] = execution_time
        results["validation_id"] = validation_id
        
        # TODO: Update validation record in database with results
        
        return results
        
    except Exception as e:
        logger.error(f"Market research failed for validation {validation_id}: {str(e)}")
        self.retry(exc=e, countdown=60)


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_experiment_generation",
    max_retries=settings.AGENT_MAX_RETRIES,
    default_retry_delay=60,
)
def run_experiment_generation(
    self,
    validation_id: str,
    business_idea: str,
    market_research: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate experiments based on market research.
    
    Args:
        validation_id: The validation request ID
        business_idea: The business idea
        market_research: Results from market research
        
    Returns:
        Experiment generation results
    """
    try:
        logger.info(f"Starting experiment generation for validation {validation_id}")
        start_time = time.time()
        
        # Initialize and run the experiment generator agent
        agent = ExperimentGeneratorAgent()
        
        # Run async method in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(
                agent.generate_experiments(
                    business_idea=business_idea,
                    market_research=market_research
                )
            )
        finally:
            loop.close()
        
        execution_time = time.time() - start_time
        logger.info(f"Experiment generation completed in {execution_time:.2f} seconds")
        
        # Add metadata
        results["execution_time_seconds"] = execution_time
        results["validation_id"] = validation_id
        
        # TODO: Update validation record in database with results
        
        return results
        
    except Exception as e:
        logger.error(f"Experiment generation failed for validation {validation_id}: {str(e)}")
        self.retry(exc=e, countdown=60)


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_marketing_campaigns",
    max_retries=settings.AGENT_MAX_RETRIES,
    default_retry_delay=60,
)
def run_marketing_campaigns(
    self,
    validation_id: str,
    business_idea: str,
    market_research: Dict[str, Any],
    experiments: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Create marketing campaigns based on research and experiments.
    
    Args:
        validation_id: The validation request ID
        business_idea: The business idea
        market_research: Results from market research
        experiments: Results from experiment generation
        
    Returns:
        Marketing campaign results
    """
    try:
        logger.info(f"Starting marketing campaign creation for validation {validation_id}")
        start_time = time.time()
        
        # Initialize and run the marketing autopilot agent
        agent = MarketingAutopilotAgent()
        
        # Run async method in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(
                agent.generate_campaigns(
                    business_idea=business_idea,
                    market_research=market_research,
                    experiment_results=experiments
                )
            )
        finally:
            loop.close()
        
        execution_time = time.time() - start_time
        logger.info(f"Marketing campaign creation completed in {execution_time:.2f} seconds")
        
        # Add metadata
        results["execution_time_seconds"] = execution_time
        results["validation_id"] = validation_id
        
        # TODO: Update validation record in database with results
        
        return results
        
    except Exception as e:
        logger.error(f"Marketing campaign creation failed for validation {validation_id}: {str(e)}")
        self.retry(exc=e, countdown=60)


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_experiment_generation_after_research",
)
def run_experiment_generation_after_research(
    self,
    validation_id: str,
    business_idea: str,
    market_research_results: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Run experiment generation after market research completes.
    
    This is a helper task for the pipeline.
    """
    # Run experiment generation with market research results
    experiment_result = run_experiment_generation.apply_async(
        args=[validation_id, business_idea, market_research_results]
    )
    
    return {
        "validation_id": validation_id,
        "experiment_task_id": experiment_result.id,
        "market_research": market_research_results
    }


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_marketing_after_experiments",
)
def run_marketing_after_experiments(
    self,
    validation_id: str,
    business_idea: str,
    pipeline_results: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Run marketing campaigns after experiments complete.
    
    This is a helper task for the pipeline.
    """
    market_research = pipeline_results.get("market_research", {})
    experiments = pipeline_results.get("experiments", {})
    
    # Run marketing campaigns with all results
    marketing_result = run_marketing_campaigns.apply_async(
        args=[validation_id, business_idea, market_research, experiments]
    )
    
    return {
        "validation_id": validation_id,
        "marketing_task_id": marketing_result.id,
        "pipeline_complete": False
    }


@celery_app.task(
    base=ValidationTask,
    bind=True,
    name="app.tasks.validation.run_full_validation",
)
def run_full_validation(
    self,
    validation_id: str,
    business_idea: str,
    target_market: str = None,
    industry: str = None,
) -> Dict[str, Any]:
    """
    Run the complete validation pipeline.
    
    This orchestrates:
    1. Market research
    2. Experiment generation (depends on market research)
    3. Marketing campaign creation (depends on both above)
    
    Args:
        validation_id: The validation request ID
        business_idea: The business idea to validate
        target_market: Optional target market
        industry: Optional industry
        
    Returns:
        Complete validation results
    """
    from celery import chain
    
    # Create a proper chain where each task receives the previous result
    # We'll need to modify tasks to handle chained inputs or use callbacks
    
    # For now, let's use a simpler approach with callbacks
    logger.info(f"Starting full validation pipeline for {validation_id}")
    
    # Step 1: Run market research
    market_research_task = run_market_research.apply_async(
        args=[validation_id, business_idea, target_market, industry],
        link=run_experiment_generation_chain.s(validation_id, business_idea)
    )
    
    return {
        "validation_id": validation_id,
        "workflow_id": market_research_task.id,
        "status": "processing",
        "message": "Validation pipeline started. Market research in progress."
    }


@celery_app.task(name="app.tasks.validation.run_experiment_generation_chain")
def run_experiment_generation_chain(market_research_results, validation_id, business_idea):
    """Chain task to run experiments after market research."""
    experiment_task = run_experiment_generation.apply_async(
        args=[validation_id, business_idea, market_research_results],
        link=run_marketing_campaigns_chain.s(validation_id, business_idea, market_research_results)
    )
    return experiment_task.id


@celery_app.task(name="app.tasks.validation.run_marketing_campaigns_chain")
def run_marketing_campaigns_chain(experiment_results, validation_id, business_idea, market_research_results):
    """Chain task to run marketing after experiments."""
    marketing_task = run_marketing_campaigns.apply_async(
        args=[validation_id, business_idea, market_research_results, experiment_results]
    )
    return marketing_task.id