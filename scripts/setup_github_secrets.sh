#!/bin/bash

# Script to help set up GitHub secrets
echo "🔐 GitHub Secrets Setup Guide"
echo "============================="
echo ""
echo "Go to: https://github.com/tudorsaitoc/validateio/settings/secrets/actions"
echo "Click 'New repository secret' for each of these:"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}CRITICAL SECRETS (Required for deployment):${NC}"
echo ""

echo "1️⃣ GCP_PROJECT_ID"
echo "   Value: Your Google Cloud Project ID"
echo "   Find it at: https://console.cloud.google.com/"
echo "   Example: my-project-123456"
echo ""

echo "2️⃣ GCP_REGION"
echo "   Value: us-central1"
echo "   (or your preferred region)"
echo ""

echo "3️⃣ GCP_SA_KEY"
echo "   Value: Your service account JSON key"
echo "   How to create:"
echo "   1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts"
echo "   2. Create a service account or use existing"
echo "   3. Add these roles:"
echo "      - Cloud Run Admin"
echo "      - Storage Admin"
echo "      - Service Account User"
echo "   4. Create key (JSON format)"
echo "   5. Copy entire JSON content as secret value"
echo ""

echo -e "${YELLOW}DATABASE SECRETS (You already have these in .env):${NC}"
echo ""

# Read from .env file
if [ -f backend/.env ]; then
    echo "4️⃣ DATABASE_URL"
    echo "   Current value in .env:"
    grep "^DATABASE_URL=" backend/.env | cut -d= -f2 | head -c 50
    echo "..."
    echo ""
    
    echo "5️⃣ SUPABASE_URL"
    echo "   Current value in .env:"
    grep "^SUPABASE_URL=" backend/.env | cut -d= -f2
    echo ""
    
    echo "6️⃣ SUPABASE_ANON_KEY"
    echo "   Current value in .env:"
    grep "^SUPABASE_ANON_KEY=" backend/.env | cut -d= -f2 | head -c 50
    echo "..."
    echo ""
    
    echo "7️⃣ SUPABASE_SERVICE_KEY"
    echo "   Current value in .env:"
    grep "^SUPABASE_SERVICE_KEY=" backend/.env | cut -d= -f2 | head -c 50
    echo "..."
    echo ""
    
    echo "8️⃣ OPENAI_API_KEY"
    echo "   Current value in .env:"
    grep "^OPENAI_API_KEY=" backend/.env | cut -d= -f2 | head -c 20
    echo "..."
    echo ""
fi

echo -e "${GREEN}OPTIONAL SECRETS:${NC}"
echo ""

echo "9️⃣ JWT_SECRET_KEY"
echo "   Generate with: openssl rand -hex 32"
openssl rand -hex 32
echo ""

echo "🔟 REDIS_URL"
echo "   Value: redis://redis:6379/0"
echo "   (or your Redis URL if using external Redis)"
echo ""

echo "1️⃣1️⃣ VERCEL_TOKEN (for frontend deployment)"
echo "   Get from: https://vercel.com/account/tokens"
echo ""

echo "1️⃣2️⃣ NEXT_PUBLIC_API_URL"
echo "   Value: https://validateio-backend-[YOUR-PROJECT].run.app"
echo "   (Will be available after first deployment)"
echo ""

echo -e "${YELLOW}Quick Copy Commands:${NC}"
echo ""
echo "Copy these values from your .env file to GitHub secrets:"
echo ""

if [ -f backend/.env ]; then
    echo "DATABASE_URL:"
    grep "^DATABASE_URL=" backend/.env | cut -d= -f2
    echo ""
    
    echo "SUPABASE_URL:"
    grep "^SUPABASE_URL=" backend/.env | cut -d= -f2
    echo ""
    
    echo "SUPABASE_ANON_KEY:"
    grep "^SUPABASE_ANON_KEY=" backend/.env | cut -d= -f2
    echo ""
    
    echo "SUPABASE_SERVICE_KEY:"
    grep "^SUPABASE_SERVICE_KEY=" backend/.env | cut -d= -f2
    echo ""
    
    echo "OPENAI_API_KEY:"
    grep "^OPENAI_API_KEY=" backend/.env | cut -d= -f2
    echo ""
fi

echo "📝 After adding secrets:"
echo "1. Re-run the GitHub Actions workflow"
echo "2. Check the deployment logs"
echo "3. Test your API with ./scripts/test_api.sh"