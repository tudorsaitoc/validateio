#!/bin/bash

# ValidateIO API Test Script
API_URL="https://validateio-847973892251.us-central1.run.app"

echo "🧪 ValidateIO API Test Suite"
echo "🔗 Testing: $API_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Basic Health Check
echo "1️⃣ Testing Basic Health Endpoint"
echo "================================"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$API_URL/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Health check passed (HTTP $HTTP_CODE)${NC}"
    echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
else
    echo -e "${RED}❌ Health check failed (HTTP $HTTP_CODE)${NC}"
    echo "$BODY"
fi

# Test 2: Detailed Health Check
echo ""
echo "2️⃣ Testing Detailed Health Endpoint"
echo "===================================="
DETAILED_RESPONSE=$(curl -s "$API_URL/health/detailed")
echo "$DETAILED_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$DETAILED_RESPONSE"

# Test 3: Create a Validation
echo ""
echo "3️⃣ Creating a Test Validation"
echo "============================="
VALIDATION_JSON='{
    "idea_description": "CoffeeSpot - An AI-powered app that helps remote workers find the perfect coffee shop for productivity. It analyzes wifi speed, noise levels, seating availability, and matches coffee preferences to mood.",
    "target_audience": "Remote workers, digital nomads, and freelancers who work from coffee shops",
    "problem_statement": "Remote workers waste 30+ minutes daily searching for suitable coffee shops with reliable wifi, good seating, and the right work environment",
    "value_proposition": "Save 30 minutes daily and boost productivity by instantly finding your perfect work-friendly coffee spot",
    "market_size": "$165 billion global coffee shop market with 35% of workforce now remote",
    "competitors": ["Yelp", "Google Maps", "Foursquare", "WorkFrom"],
    "unique_features": ["Real-time wifi speed testing", "AI mood-to-coffee matching", "Productivity scoring", "Crowd-sourced noise levels"],
    "revenue_model": "Freemium app with premium features at $4.99/month plus affiliate commissions",
    "validation_type": "full",
    "timeline_days": 30
}'

echo "Sending validation request..."
VALIDATION_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/validations" \
    -H "Content-Type: application/json" \
    -d "$VALIDATION_JSON")

# Check if response contains an ID
if echo "$VALIDATION_RESPONSE" | grep -q '"id"'; then
    echo -e "${GREEN}✅ Validation created successfully!${NC}"
    echo "$VALIDATION_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$VALIDATION_RESPONSE"
    
    # Extract validation ID
    VALIDATION_ID=$(echo "$VALIDATION_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)
    
    if [ ! -z "$VALIDATION_ID" ]; then
        echo ""
        echo "Validation ID: $VALIDATION_ID"
        
        # Wait and check status
        echo ""
        echo "4️⃣ Checking Validation Status (after 5 seconds)"
        echo "=============================================="
        sleep 5
        
        STATUS_RESPONSE=$(curl -s "$API_URL/api/v1/validations/$VALIDATION_ID")
        echo "$STATUS_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$STATUS_RESPONSE"
    fi
else
    echo -e "${RED}❌ Failed to create validation${NC}"
    echo "$VALIDATION_RESPONSE"
fi

# Test 5: List Validations
echo ""
echo "5️⃣ Listing All Validations"
echo "========================="
LIST_RESPONSE=$(curl -s "$API_URL/api/v1/validations")
if echo "$LIST_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'Found {len(data)} validations')" 2>/dev/null; then
    echo -e "${GREEN}✅ Successfully retrieved validations${NC}"
else
    echo -e "${RED}❌ Failed to list validations${NC}"
    echo "$LIST_RESPONSE"
fi

# Test 6: API Documentation
echo ""
echo "6️⃣ API Documentation Links"
echo "========================="
echo "📚 Interactive API Docs: $API_URL/docs"
echo "📚 ReDoc Documentation: $API_URL/redoc"
echo ""
echo "You can open these in your browser to explore all available endpoints!"

echo ""
echo "✅ API Test Complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Check the validation status in a few minutes"
echo "2. Explore the API docs at $API_URL/docs"
echo "3. Build a frontend to create and view validations"
echo "4. Monitor agent processing in Cloud Run logs"