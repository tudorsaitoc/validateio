#!/usr/bin/env python3
"""
Quick test script to verify AI agents are working.
Run this after setting up your environment.
"""

import asyncio
import os
from pathlib import Path

# Simple test without heavy imports
def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment...\n")
    
    # Check Python version
    import sys
    print(f"Python version: {sys.version}")
    
    # Check for .env file
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file not found - creating from example...")
        example_env = Path(__file__).parent.parent / ".env.example"
        if example_env.exists():
            import shutil
            shutil.copy(example_env, env_path)
            print("📋 Created .env from .env.example")
        else:
            print("❌ .env.example not found!")
            return False
    
    # Check for OpenAI API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        print("✅ OpenAI API key configured")
        return True
    else:
        print("❌ OpenAI API key not configured!")
        print("\nPlease add your OpenAI API key to backend/.env:")
        print("OPENAI_API_KEY=sk-your-key-here")
        return False


async def test_market_research():
    """Test just the market research agent."""
    print("\n🧪 Testing Market Research Agent...\n")
    
    try:
        from app.agents import MarketResearchAgent
        
        agent = MarketResearchAgent()
        results = await agent.research(
            business_idea="AI-powered personal finance app for millennials",
            target_market="Tech-savvy millennials aged 25-35",
            industry="FinTech"
        )
        
        print("✅ Market Research completed!")
        print(f"Found {len(results.get('competitors', []))} competitors")
        print(f"Market size TAM: ${results.get('market_size', {}).get('tam', 0):,.0f}")
        print(f"Confidence score: {results.get('confidence_score', 0):.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


async def main():
    """Run the quick test."""
    print("🚀 ValidateIO Quick Test\n")
    
    if not check_environment():
        print("\n⚠️  Please fix the environment issues above and try again.")
        return
    
    print("\nEnvironment looks good! Testing AI agent...\n")
    
    success = await test_market_research()
    
    if success:
        print("\n✅ All tests passed! ValidateIO is ready to use.")
        print("\nNext steps:")
        print("1. Run the full pipeline test: python test_validation_pipeline.py")
        print("2. Start the API server: python -m uvicorn main:app --reload")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")


if __name__ == "__main__":
    asyncio.run(main())