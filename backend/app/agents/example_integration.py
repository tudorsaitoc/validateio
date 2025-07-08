"""
Example integration showing how to use ExperimentGeneratorAgent
in the ValidateIO validation workflow.
"""

import asyncio
from typing import Dict, Any

from app.agents import MarketResearchAgent, ExperimentGeneratorAgent
from app.schemas.validation import ValidationCreate


async def run_validation_workflow(validation_data: ValidationCreate) -> Dict[str, Any]:
    """
    Run the complete validation workflow.
    
    This example shows how the ExperimentGeneratorAgent integrates
    with the MarketResearchAgent in the validation pipeline.
    """
    results = {}
    
    # Step 1: Market Research
    print("Step 1: Conducting market research...")
    market_research_agent = MarketResearchAgent()
    market_research_results = await market_research_agent.research(
        business_idea=validation_data.business_idea,
        target_market=validation_data.target_market,
        industry=validation_data.industry
    )
    results["market_research"] = market_research_results
    
    # Step 2: Generate Experiments
    print("Step 2: Generating experiments based on market research...")
    experiment_agent = ExperimentGeneratorAgent()
    experiment_results = await experiment_agent.generate_experiments(
        business_idea=validation_data.business_idea,
        market_research=market_research_results,
        target_market=validation_data.target_market,
        industry=validation_data.industry
    )
    results["experiments"] = experiment_results
    
    # Step 3: Marketing Campaigns (placeholder for future agent)
    print("Step 3: Marketing campaigns generation (not yet implemented)")
    results["marketing_campaigns"] = {
        "status": "not_implemented",
        "message": "Marketing campaign agent coming soon"
    }
    
    return results


# Example usage
if __name__ == "__main__":
    # Sample validation request
    validation = ValidationCreate(
        business_idea="A mobile app that uses AI to help small restaurants optimize their menu pricing based on local competition and demand patterns",
        target_market="Small independent restaurants in urban areas",
        industry="Restaurant Tech"
    )
    
    # Run the workflow
    async def main():
        results = await run_validation_workflow(validation)
        
        print("\n=== VALIDATION WORKFLOW COMPLETE ===")
        print(f"\nMarket Research Confidence: {results['market_research']['confidence_score']}")
        print(f"Predicted Conversion Rate: {results['experiments']['predicted_conversion_rate']}%")
        print(f"\nKey Findings:")
        print(f"- Competitors identified: {len(results['market_research']['competitors'])}")
        print(f"- Landing page variations: {len(results['experiments']['landing_pages'])}")
        print(f"- A/B tests designed: {len(results['experiments']['ab_tests'])}")
        print(f"- Target audiences: {len(results['experiments']['target_audiences'])}")
    
    asyncio.run(main())