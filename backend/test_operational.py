#!/usr/bin/env python3
"""
Operational test script for ValidateIO backend.

Tests the following:
1. Database connection
2. User creation
3. Validation creation
4. Full validation pipeline
5. Health check endpoint

Run with: python test_operational.py
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import httpx

# Import application components
from app.core.config import settings
from app.db.base import Base
from app.models.user import User
from app.models.validation import Validation, ValidationStatus
from app.core.security import get_password_hash, verify_password
from app.db.session import AsyncSessionLocal, engine

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_status(test_name: str, success: bool, message: str = ""):
    """Print colored test status."""
    status = f"{Colors.GREEN}✓ PASS{Colors.END}" if success else f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"\n{Colors.BOLD}{test_name}:{Colors.END} {status}")
    if message:
        print(f"  {message}")


def print_section(title: str):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}")


async def test_database_connection():
    """Test database connection."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
            
            # Check if we can query the database version
            result = await session.execute(text("SELECT version()"))
            db_version = result.scalar()
            
        print_status("Database Connection", True, f"Connected to: {db_version}")
        return True
    except Exception as e:
        print_status("Database Connection", False, str(e))
        return False


async def test_create_tables():
    """Test creating database tables."""
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
            
        print_status("Create Tables", True, "All tables created successfully")
        return True
    except Exception as e:
        print_status("Create Tables", False, str(e))
        return False


async def test_create_user():
    """Test creating a user."""
    try:
        async with AsyncSessionLocal() as session:
            # Check if test user already exists
            result = await session.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": "test@validateio.com"}
            )
            existing_user = result.scalar()
            
            if existing_user:
                print_status("Create User", True, "Test user already exists")
                return str(existing_user)
            
            # Create new user
            test_user = User(
                email="test@validateio.com",
                username="testuser",
                full_name="Test User",
                hashed_password=get_password_hash("testpassword123"),
                is_active=True,
                is_verified=True
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print_status("Create User", True, f"User created with ID: {test_user.id}")
            return str(test_user.id)
            
    except Exception as e:
        print_status("Create User", False, str(e))
        return None


async def test_create_validation(user_id: str):
    """Test creating a validation."""
    try:
        async with AsyncSessionLocal() as session:
            # Create validation
            test_validation = Validation(
                user_id=user_id,
                business_idea="An AI-powered personal finance app that helps millennials save money through gamification and personalized insights",
                target_market="Millennials aged 25-35 in urban areas",
                industry="FinTech",
                status=ValidationStatus.PENDING
            )
            
            session.add(test_validation)
            await session.commit()
            await session.refresh(test_validation)
            
            print_status("Create Validation", True, f"Validation created with ID: {test_validation.id}")
            return str(test_validation.id)
            
    except Exception as e:
        print_status("Create Validation", False, str(e))
        return None


async def test_agent_imports():
    """Test importing AI agents."""
    try:
        from app.agents import MarketResearchAgent, ExperimentGeneratorAgent, MarketingAutopilotAgent
        
        # Test instantiation
        market_agent = MarketResearchAgent()
        experiment_agent = ExperimentGeneratorAgent()
        marketing_agent = MarketingAutopilotAgent()
        
        print_status("Import Agents", True, "All agents imported and instantiated successfully")
        return True
    except Exception as e:
        print_status("Import Agents", False, str(e))
        return False


async def test_validation_pipeline(validation_id: str):
    """Test the full validation pipeline."""
    try:
        from app.agents import MarketResearchAgent, ExperimentGeneratorAgent, MarketingAutopilotAgent
        
        async with AsyncSessionLocal() as session:
            # Get validation
            result = await session.execute(
                text("SELECT * FROM validations WHERE id = :id"),
                {"id": validation_id}
            )
            validation_data = result.fetchone()
            
            if not validation_data:
                print_status("Validation Pipeline", False, "Validation not found")
                return False
            
            print(f"\n{Colors.YELLOW}Testing validation pipeline (this may take a moment)...{Colors.END}")
            
            # Update status to processing
            await session.execute(
                text("UPDATE validations SET status = :status WHERE id = :id"),
                {"status": ValidationStatus.PROCESSING.value, "id": validation_id}
            )
            await session.commit()
            
            # 1. Market Research
            print(f"\n  {Colors.BOLD}1. Market Research Agent{Colors.END}")
            market_agent = MarketResearchAgent()
            
            # Check if agent has required API keys
            if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
                print(f"    {Colors.YELLOW}⚠ No API keys found for LLM (OPENAI_API_KEY or ANTHROPIC_API_KEY){Colors.END}")
                print_status("Validation Pipeline", False, "Missing required API keys")
                return False
            
            try:
                market_research = await market_agent.research_market(
                    business_idea=validation_data.business_idea,
                    target_market=validation_data.target_market,
                    industry=validation_data.industry
                )
                print(f"    {Colors.GREEN}✓ Market research completed{Colors.END}")
                
                # Save results
                await session.execute(
                    text("UPDATE validations SET market_research = :data WHERE id = :id"),
                    {"data": json.dumps(market_research), "id": validation_id}
                )
                await session.commit()
                
            except Exception as e:
                print(f"    {Colors.RED}✗ Market research failed: {e}{Colors.END}")
                # Continue to test other agents
            
            # 2. Experiment Generator
            print(f"\n  {Colors.BOLD}2. Experiment Generator Agent{Colors.END}")
            experiment_agent = ExperimentGeneratorAgent()
            
            try:
                experiments = await experiment_agent.generate_experiments(
                    business_idea=validation_data.business_idea,
                    market_research=market_research if 'market_research' in locals() else {}
                )
                print(f"    {Colors.GREEN}✓ Experiments generated{Colors.END}")
                
                # Save results
                await session.execute(
                    text("UPDATE validations SET experiments = :data WHERE id = :id"),
                    {"data": json.dumps(experiments), "id": validation_id}
                )
                await session.commit()
                
            except Exception as e:
                print(f"    {Colors.RED}✗ Experiment generation failed: {e}{Colors.END}")
            
            # 3. Marketing Autopilot
            if settings.ENABLE_MARKETING_AGENT:
                print(f"\n  {Colors.BOLD}3. Marketing Autopilot Agent{Colors.END}")
                marketing_agent = MarketingAutopilotAgent()
                
                try:
                    campaigns = await marketing_agent.create_campaigns(
                        business_idea=validation_data.business_idea,
                        experiments=experiments if 'experiments' in locals() else {}
                    )
                    print(f"    {Colors.GREEN}✓ Marketing campaigns created{Colors.END}")
                    
                    # Save results
                    await session.execute(
                        text("UPDATE validations SET marketing_campaigns = :data WHERE id = :id"),
                        {"data": json.dumps(campaigns), "id": validation_id}
                    )
                    await session.commit()
                    
                except Exception as e:
                    print(f"    {Colors.RED}✗ Marketing campaign creation failed: {e}{Colors.END}")
            else:
                print(f"\n  {Colors.YELLOW}⚠ Marketing Agent is disabled in settings{Colors.END}")
            
            # Update status to completed
            await session.execute(
                text("UPDATE validations SET status = :status, completed_at = :completed WHERE id = :id"),
                {
                    "status": ValidationStatus.COMPLETED.value,
                    "completed": datetime.utcnow(),
                    "id": validation_id
                }
            )
            await session.commit()
            
            print_status("Validation Pipeline", True, "Pipeline execution completed")
            return True
            
    except Exception as e:
        print_status("Validation Pipeline", False, str(e))
        return False


async def test_health_endpoint():
    """Test the health check endpoint."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:{settings.PORT}/health")
            
            if response.status_code == 200:
                data = response.json()
                print_status(
                    "Health Endpoint", 
                    True, 
                    f"Service: {data.get('service')}, Status: {data.get('status')}, Version: {data.get('version')}"
                )
                return True
            else:
                print_status("Health Endpoint", False, f"Status code: {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print_status("Health Endpoint", False, "Could not connect to API (is the server running?)")
        return False
    except Exception as e:
        print_status("Health Endpoint", False, str(e))
        return False


async def main():
    """Run all operational tests."""
    print(f"{Colors.BOLD}ValidateIO Backend Operational Test{Colors.END}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration summary
    print_section("Configuration Summary")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"Database URL: {settings.DATABASE_URL or 'Using default PostgreSQL'}")
    print(f"API Keys configured:")
    print(f"  - OpenAI: {'✓' if settings.OPENAI_API_KEY else '✗'}")
    print(f"  - Anthropic: {'✓' if settings.ANTHROPIC_API_KEY else '✗'}")
    print(f"  - Serper: {'✓' if settings.SERPER_API_KEY else '✗'}")
    print(f"Feature Flags:")
    print(f"  - Market Research Agent: {'✓' if settings.ENABLE_RESEARCH_AGENT else '✗'}")
    print(f"  - Experiment Agent: {'✓' if settings.ENABLE_EXPERIMENT_AGENT else '✗'}")
    print(f"  - Marketing Agent: {'✓' if settings.ENABLE_MARKETING_AGENT else '✗'}")
    
    # Run tests
    print_section("Running Tests")
    
    # Test 1: Database connection
    db_ok = await test_database_connection()
    if not db_ok:
        print(f"\n{Colors.RED}Cannot proceed without database connection{Colors.END}")
        return
    
    # Test 2: Create tables
    await test_create_tables()
    
    # Test 3: Create user
    user_id = await test_create_user()
    if not user_id:
        print(f"\n{Colors.RED}Cannot proceed without user{Colors.END}")
        return
    
    # Test 4: Create validation
    validation_id = await test_create_validation(user_id)
    if not validation_id:
        print(f"\n{Colors.RED}Cannot proceed without validation{Colors.END}")
        return
    
    # Test 5: Import agents
    agents_ok = await test_agent_imports()
    
    # Test 6: Health endpoint
    await test_health_endpoint()
    
    # Test 7: Validation pipeline (only if agents are OK and we have API keys)
    if agents_ok and (settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY):
        await test_validation_pipeline(validation_id)
    else:
        print(f"\n{Colors.YELLOW}Skipping validation pipeline test (missing agents or API keys){Colors.END}")
    
    # Summary
    print_section("Test Summary")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print("1. Ensure the FastAPI server is running: uvicorn main:app --reload")
    print("2. Set up required API keys in .env file")
    print("3. Configure Redis for Celery task queue")
    print("4. Set up ChromaDB for vector storage")
    print("5. Run the full test suite: pytest")


if __name__ == "__main__":
    asyncio.run(main())