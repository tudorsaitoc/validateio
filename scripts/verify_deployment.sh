#!/bin/bash

# Deployment verification script
echo "🔍 ValidateIO Deployment Verification"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get Cloud Run URL
echo "Enter your Cloud Run service URL (e.g., https://validateio-backend-xxx.run.app):"
read -p "URL: " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}❌ No URL provided${NC}"
    exit 1
fi

echo ""
echo "1️⃣ Testing health endpoint..."
if curl -s -f "$BACKEND_URL/health" > /dev/null; then
    echo -e "${GREEN}✅ Health endpoint accessible${NC}"
    echo "Response:"
    curl -s "$BACKEND_URL/health" | python3 -m json.tool
else
    echo -e "${RED}❌ Health endpoint not accessible${NC}"
    exit 1
fi

echo ""
echo "2️⃣ Testing detailed health..."
DETAILED_RESPONSE=$(curl -s "$BACKEND_URL/health/detailed")
echo "Response:"
echo "$DETAILED_RESPONSE" | python3 -m json.tool

# Check component status
echo ""
echo "3️⃣ Component Status:"
echo "$DETAILED_RESPONSE" | python3 -c "
import json, sys
data = json.load(sys.stdin)
components = data.get('components', {})
for name, status in components.items():
    if status.get('status') == 'healthy' or status == 'configured':
        print(f'✅ {name}: OK')
    else:
        print(f'❌ {name}: {status}')
"

echo ""
echo "4️⃣ Testing API documentation..."
if curl -s -f "$BACKEND_URL/docs" > /dev/null; then
    echo -e "${GREEN}✅ API docs accessible at: $BACKEND_URL/docs${NC}"
else
    echo -e "${YELLOW}⚠️  API docs not accessible${NC}"
fi

echo ""
echo "5️⃣ Testing frontend (if deployed)..."
echo "Enter your Vercel frontend URL (or press Enter to skip):"
read -p "URL: " FRONTEND_URL

if [ ! -z "$FRONTEND_URL" ]; then
    if curl -s -f "$FRONTEND_URL" > /dev/null; then
        echo -e "${GREEN}✅ Frontend accessible at: $FRONTEND_URL${NC}"
    else
        echo -e "${RED}❌ Frontend not accessible${NC}"
    fi
fi

echo ""
echo "📋 Summary:"
echo "- Backend API: $BACKEND_URL"
echo "- API Docs: $BACKEND_URL/docs"
echo "- Health Check: $BACKEND_URL/health"
if [ ! -z "$FRONTEND_URL" ]; then
    echo "- Frontend: $FRONTEND_URL"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Update your local .env with the deployed URLs"
echo "2. Test creating a validation via the API"
echo "3. Monitor logs in Google Cloud Console"
echo "4. Set up local development to use Supabase"