"""Test script for ExperimentGeneratorAgent"""

import asyncio
import json
from app.agents import ExperimentGeneratorAgent

async def test_experiment_agent():
    # Initialize the agent
    agent = ExperimentGeneratorAgent()
    
    # Sample business idea and market research data
    business_idea = "An AI-powered personal finance app that helps millennials save money"
    
    market_research = {
        "competitors": [
            {
                "name": "Mint",
                "description": "Personal finance management app",
                "strengths": ["Free", "Bank integration", "Budgeting tools"],
                "weaknesses": ["Complex UI", "Limited AI features"]
            },
            {
                "name": "YNAB",
                "description": "You Need A Budget - budgeting app",
                "strengths": ["Zero-based budgeting", "Educational content"],
                "weaknesses": ["Subscription cost", "Learning curve"]
            }
        ],
        "customer_pain_points": [
            "Difficulty tracking spending across multiple accounts",
            "Lack of personalized savings recommendations",
            "No proactive alerts for overspending",
            "Complex budgeting tools that are hard to use",
            "Limited insights into spending patterns"
        ],
        "unique_value_proposition": "The only finance app that uses AI to automatically find and execute personalized micro-savings opportunities based on your spending patterns",
        "market_trends": [
            "Growing adoption of AI in personal finance",
            "Millennials seeking automated financial solutions",
            "Increased focus on financial wellness",
            "Rise of micro-investing and micro-savings",
            "Gamification of financial habits"
        ]
    }
    
    # Generate experiments
    print("Generating experiments...")
    try:
        results = await agent.generate_experiments(
            business_idea=business_idea,
            market_research=market_research,
            target_market="Millennials aged 25-35 in urban areas",
            industry="FinTech"
        )
        
        # Print results
        print("\n=== EXPERIMENT GENERATION RESULTS ===\n")
        
        print(f"Predicted Conversion Rate: {results['predicted_conversion_rate']}%")
        print(f"Confidence Score: {results['confidence_score']}")
        print(f"\nRationale: {results['rationale']}")
        
        print(f"\n=== LANDING PAGE VARIATIONS ({len(results['landing_pages'])}) ===")
        for lp in results['landing_pages']:
            print(f"\nVariant {lp['variant_id']}:")
            print(f"  Headline: {lp['headline']}")
            print(f"  CTA: {lp['cta_text']}")
            print(f"  Design: {lp['design_style']}")
        
        print(f"\n=== A/B TESTS ({len(results['ab_tests'])}) ===")
        for test in results['ab_tests']:
            print(f"\n{test['test_name']}:")
            print(f"  Hypothesis: {test['hypothesis']}")
            print(f"  Metric: {test['primary_metric']}")
            print(f"  Sample Size: {test['minimum_sample_size']} per variant")
        
        print(f"\n=== COPY VARIATIONS ({len(results['copy_variations'])}) ===")
        for copy in results['copy_variations']:
            print(f"\nVariant {copy['variant_id']} ({copy['tone']}):")
            print(f"  Headline: {copy['headline']}")
            print(f"  CTA: {copy['cta_copy']}")
        
        print(f"\n=== TARGET AUDIENCES ({len(results['target_audiences'])}) ===")
        for audience in results['target_audiences']:
            print(f"\n{audience['segment_name']}:")
            print(f"  Size: {audience['estimated_size']:,}")
            print(f"  Channels: {', '.join(audience['channels'])}")
            print(f"  Approach: {audience['messaging_approach']}")
        
        # Save full results to file
        with open('experiment_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("\n\nFull results saved to experiment_results.json")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_experiment_agent())