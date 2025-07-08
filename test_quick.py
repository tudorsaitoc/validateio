#!/usr/bin/env python3
"""
Quick test of ValidateIO AI pipeline
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

import os
os.chdir(backend_path)

from app.agents import MarketResearchAgent


async def quick_test():
    print("🧪 Quick ValidateIO Test")
    print("========================\n")
    
    # Check API key
    from app.core.config import settings
    if not settings.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not configured!")
        return
    
    print("✅ API Key configured\n")
    
    # Test Market Research Agent
    print("Testing Market Research Agent...")
    try:
        agent = MarketResearchAgent()
        results = await agent.research(
            business_idea="AI-powered personal finance app for millennials",
            target_market="Tech-savvy millennials aged 25-35",
            industry="FinTech"
        )
        
        print("\n✅ Market Research Results:")
        print(f"- Competitors found: {len(results.get('competitors', []))}")
        print(f"- Market size TAM: ${results.get('market_size', {}).get('tam', 0):,.0f}")
        print(f"- Pain points: {len(results.get('customer_pain_points', []))}")
        print(f"- Market trends: {len(results.get('market_trends', []))}")
        print(f"- Confidence score: {results.get('confidence_score', 0)}")
        
        if results.get('unique_value_proposition'):
            print(f"\nValue Proposition: {results['unique_value_proposition']}")
        
        print("\n🎉 ValidateIO is working! The AI agents are operational.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure your OpenAI API key is valid")
        print("2. Check your internet connection")
        print("3. Try running: pip install openai langchain langchain-openai")


if __name__ == "__main__":
    asyncio.run(quick_test())