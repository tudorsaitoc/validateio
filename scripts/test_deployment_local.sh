#!/bin/bash

echo "🧪 Local Deployment Test"
echo "======================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "1️⃣ Testing Docker build locally..."
cd backend

# Test if Dockerfile exists
if [ ! -f Dockerfile ]; then
    echo -e "${RED}❌ Dockerfile not found in backend/${NC}"
    exit 1
fi

# Test Docker build
echo "Building Docker image..."
if docker build -t validateio-test .; then
    echo -e "${GREEN}✅ Docker build successful${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

echo ""
echo "2️⃣ Testing local run..."
echo "Starting container..."

# Load env vars from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run container
docker run -d --name validateio-test-run \
    -p 8000:8000 \
    -e DATABASE_URL="$DATABASE_URL" \
    -e SUPABASE_URL="$SUPABASE_URL" \
    -e SUPABASE_ANON_KEY="$SUPABASE_ANON_KEY" \
    -e OPENAI_API_KEY="$OPENAI_API_KEY" \
    -e JWT_SECRET_KEY="${JWT_SECRET_KEY:-$(openssl rand -hex 32)}" \
    -e ENVIRONMENT="production" \
    -e USE_SUPABASE_AUTH="true" \
    validateio-test

# Wait for startup
echo "Waiting for service to start..."
sleep 5

# Test health endpoint
echo ""
echo "3️⃣ Testing health endpoint..."
if curl -f http://localhost:8000/health; then
    echo -e "\n${GREEN}✅ Health check passed${NC}"
else
    echo -e "\n${RED}❌ Health check failed${NC}"
    echo ""
    echo "Container logs:"
    docker logs validateio-test-run
fi

# Cleanup
echo ""
echo "Cleaning up..."
docker stop validateio-test-run >/dev/null 2>&1
docker rm validateio-test-run >/dev/null 2>&1

echo ""
echo "4️⃣ Common deployment issues:"
echo "- Missing environment variables (check GitHub secrets)"
echo "- Database connection issues (check DATABASE_URL)"
echo "- Port conflicts (8000 already in use)"
echo "- Memory limits (Cloud Run might need more than 1Gi)"
echo ""
echo "To see the actual error in GitHub Actions:"
echo "1. Go to: https://github.com/tudorsaitoc/validateio/actions"
echo "2. Click on the failed workflow"
echo "3. Click on the 'deploy' job"
echo "4. Expand the failed step to see the full error"