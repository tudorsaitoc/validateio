#!/usr/bin/env python3
"""
Test the complete ValidateIO validation pipeline.

This script simulates a full validation request through all three agents:
1. Market Research
2. Experiment Generation
3. Marketing Campaigns
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.agents import MarketResearchAgent, ExperimentGeneratorAgent, MarketingAutopilotAgent
from app.core.config import settings


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def print_section(title, content):
    """Print a formatted section."""
    print(f"\n{title}:")
    print("-" * len(title))
    if isinstance(content, dict):
        print(json.dumps(content, indent=2))
    elif isinstance(content, list):
        for i, item in enumerate(content, 1):
            print(f"{i}. {item}")
    else:
        print(content)


async def test_validation_pipeline():
    """Test the complete validation pipeline."""
    
    # Test input
    business_idea = "AI-powered personal finance app for millennials that uses behavioral psychology to improve saving habits"
    target_market = "Tech-savvy millennials aged 25-35 in urban areas"
    industry = "FinTech"
    
    print_header("ValidateIO Pipeline Test")
    print(f"Business Idea: {business_idea}")
    print(f"Target Market: {target_market}")
    print(f"Industry: {industry}")
    
    # Check API keys
    if not settings.OPENAI_API_KEY:
        print("\n❌ ERROR: OPENAI_API_KEY not configured!")
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    print("\n✅ API Key configured")
    
    try:
        # Step 1: Market Research
        print_header("Step 1: Market Research")
        print("Initializing Market Research Agent...")
        
        market_agent = MarketResearchAgent()
        market_results = await market_agent.research(
            business_idea=business_idea,
            target_market=target_market,
            industry=industry
        )
        
        print("✅ Market Research Complete!")
        print_section("Competitors Found", [c["name"] for c in market_results.get("competitors", [])])
        print_section("Market Size", market_results.get("market_size", {}))
        print_section("Key Pain Points", market_results.get("customer_pain_points", []))
        print_section("Market Trends", market_results.get("market_trends", []))
        print_section("Unique Value Proposition", market_results.get("unique_value_proposition", ""))
        
        # Step 2: Experiment Generation
        print_header("Step 2: Experiment Generation")
        print("Initializing Experiment Generator Agent...")
        
        experiment_agent = ExperimentGeneratorAgent()
        experiment_results = await experiment_agent.generate_experiments(
            business_idea=business_idea,
            market_research=market_results
        )
        
        print("✅ Experiments Generated!")
        print_section("Landing Page Variations", len(experiment_results.get("landing_pages", [])))
        print_section("A/B Tests", [test["name"] for test in experiment_results.get("ab_tests", [])])
        print_section("Copy Variations", len(experiment_results.get("copy_variations", [])))
        print_section("Target Audiences", [aud["name"] for aud in experiment_results.get("target_audiences", [])])
        print_section("Predicted Conversion Rate", f"{experiment_results.get('predicted_conversion_rate', 0)}%")
        
        # Step 3: Marketing Campaigns
        print_header("Step 3: Marketing Campaign Generation")
        print("Initializing Marketing Autopilot Agent...")
        
        marketing_agent = MarketingAutopilotAgent()
        marketing_results = await marketing_agent.generate_campaigns(
            business_idea=business_idea,
            market_research=market_results,
            experiments=experiment_results
        )
        
        print("✅ Marketing Campaigns Created!")
        print_section("Ad Campaigns", [f"{c['platform']} - ${c['budget']}" for c in marketing_results.get("ad_campaigns", [])])
        print_section("Content Strategy", f"{len(marketing_results.get('content_strategy', {}).get('blog_posts', []))} blog posts planned")
        print_section("Recommended Channels", marketing_results.get("channel_recommendations", []))
        print_section("Budget Allocation", marketing_results.get("budget_allocation", {}))
        print_section("Expected ROI", f"{marketing_results.get('expected_roi', 0):.1f}x")
        
        # Summary
        print_header("Pipeline Test Complete! 🎉")
        print("All three agents executed successfully:")
        print("✅ Market Research - Analyzed competitors and market opportunity")
        print("✅ Experiment Generation - Created testable variations")
        print("✅ Marketing Campaigns - Planned go-to-market strategy")
        print(f"\nTotal execution time: {datetime.now()}")
        
        # Save results
        output_file = "validation_test_results.json"
        results = {
            "timestamp": datetime.now().isoformat(),
            "input": {
                "business_idea": business_idea,
                "target_market": target_market,
                "industry": industry
            },
            "market_research": market_results,
            "experiments": experiment_results,
            "marketing_campaigns": marketing_results
        }
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Full results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting ValidateIO Pipeline Test...")
    print("This will test all three AI agents in sequence.")
    print("Note: This requires OPENAI_API_KEY to be configured.\n")
    
    # Run the async test
    asyncio.run(test_validation_pipeline())