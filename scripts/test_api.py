#!/usr/bin/env python3
"""Test the deployed ValidateIO API"""

import json
import requests
import time
from datetime import datetime

# API Configuration
API_URL = "https://validateio-847973892251.us-central1.run.app"

def test_health():
    """Test health endpoints"""
    print("🔍 Testing Health Endpoints")
    print("=" * 50)
    
    # Basic health
    response = requests.get(f"{API_URL}/health")
    print(f"\n1. Basic Health Check: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")
    
    # Detailed health
    response = requests.get(f"{API_URL}/health/detailed")
    print(f"\n2. Detailed Health Check: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        
        # Check components
        print("\n📊 Component Status:")
        components = data.get("components", {})
        for name, status in components.items():
            if isinstance(status, dict):
                status_text = status.get("status", "unknown")
                if status_text == "healthy":
                    print(f"✅ {name}: {status_text}")
                else:
                    print(f"❌ {name}: {status_text} - {status.get('error', '')}")
            else:
                print(f"✅ {name}: {status}")
    
    return response.status_code == 200

def test_create_validation():
    """Test creating a validation"""
    print("\n\n🚀 Testing Validation Creation")
    print("=" * 50)
    
    # Test idea
    validation_data = {
        "idea_description": "A mobile app that uses AI to help people find the perfect coffee shop based on their work style, coffee preferences, and current mood. It would analyze wifi speed, noise levels, seating availability, and coffee quality.",
        "target_audience": "Remote workers, digital nomads, and coffee enthusiasts who work from cafes",
        "problem_statement": "Remote workers waste time searching for suitable coffee shops with good wifi, proper seating, and the right ambiance for productivity",
        "value_proposition": "Save 30 minutes daily finding the perfect work-friendly coffee shop that matches your preferences",
        "market_size": "The global coffee shop market is worth $165 billion with 35% of workers now remote",
        "competitors": ["Yelp", "Google Maps", "Foursquare"],
        "unique_features": ["Real-time wifi speed testing", "Noise level monitoring", "Productivity score based on user work patterns", "AI-powered mood-to-coffee matching"],
        "revenue_model": "Freemium with premium features for $4.99/month, affiliate commissions from coffee shops",
        "validation_type": "full",
        "timeline_days": 30
    }
    
    print("\nSending validation request...")
    print(f"Idea: {validation_data['idea_description'][:100]}...")
    
    # Create validation
    response = requests.post(
        f"{API_URL}/api/v1/validations",
        json=validation_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code in [200, 201]:
        result = response.json()
        print("\n✅ Validation created successfully!")
        print(f"ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        print(f"Created: {result.get('created_at')}")
        
        if result.get('tasks'):
            print(f"\n📋 Tasks created: {len(result['tasks'])}")
            for task in result['tasks']:
                print(f"  - {task['agent_type']}: {task['status']}")
        
        return result.get('id')
    else:
        print(f"\n❌ Error creating validation: {response.status_code}")
        print(response.text)
        return None

def test_get_validation(validation_id):
    """Test getting validation status"""
    if not validation_id:
        return
    
    print("\n\n📊 Checking Validation Status")
    print("=" * 50)
    
    # Wait a bit for processing
    print("Waiting 5 seconds for processing...")
    time.sleep(5)
    
    response = requests.get(f"{API_URL}/api/v1/validations/{validation_id}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nValidation ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        print(f"Progress: {result.get('progress', 0)}%")
        
        # Check agent results
        if result.get('market_research_result'):
            print("\n🔍 Market Research: ✅ Complete")
            research = result['market_research_result']
            if isinstance(research, dict):
                print(f"  - Market Size: {research.get('market_size', 'N/A')}")
                print(f"  - Growth Rate: {research.get('growth_rate', 'N/A')}")
                print(f"  - Competition: {research.get('competition_level', 'N/A')}")
        
        if result.get('experiment_results'):
            print("\n🧪 Experiments: ✅ Complete")
            print(f"  - {len(result['experiment_results'])} experiments generated")
        
        if result.get('marketing_result'):
            print("\n📢 Marketing: ✅ Complete")
            marketing = result['marketing_result']
            if isinstance(marketing, dict) and marketing.get('strategies'):
                print(f"  - {len(marketing['strategies'])} strategies generated")
    else:
        print(f"❌ Error getting validation: {response.status_code}")
        print(response.text)

def test_list_validations():
    """Test listing all validations"""
    print("\n\n📋 Listing All Validations")
    print("=" * 50)
    
    response = requests.get(f"{API_URL}/api/v1/validations")
    
    if response.status_code == 200:
        validations = response.json()
        print(f"\nTotal validations: {len(validations)}")
        
        for val in validations[:5]:  # Show first 5
            print(f"\n- ID: {val.get('id')}")
            print(f"  Status: {val.get('status')}")
            print(f"  Created: {val.get('created_at')}")
            print(f"  Idea: {val.get('idea_description', '')[:80]}...")
    else:
        print(f"❌ Error listing validations: {response.status_code}")

def test_api_docs():
    """Check if API docs are accessible"""
    print("\n\n📚 API Documentation")
    print("=" * 50)
    
    response = requests.get(f"{API_URL}/docs", allow_redirects=True)
    
    if response.status_code == 200:
        print(f"✅ API docs available at: {API_URL}/docs")
        print(f"✅ ReDoc available at: {API_URL}/redoc")
    else:
        print(f"❌ API docs not accessible: {response.status_code}")

if __name__ == "__main__":
    print("🧪 ValidateIO API Test Suite")
    print(f"🔗 Testing: {API_URL}")
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n")
    
    # Run tests
    if test_health():
        validation_id = test_create_validation()
        if validation_id:
            test_get_validation(validation_id)
        test_list_validations()
    
    test_api_docs()
    
    print("\n\n✅ Test suite complete!")
    print(f"🕐 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")