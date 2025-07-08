#!/bin/bash

# Quick deployment verification script

echo "🔍 ValidateIO Deployment Verification"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check environment variables
echo "1️⃣ Checking Environment Variables..."
echo ""

check_env() {
    if [ -f "backend/.env" ]; then
        if grep -q "$1=" backend/.env; then
            echo -e "  $1: ${GREEN}✓ Configured${NC}"
            return 0
        else
            echo -e "  $1: ${RED}✗ Not found${NC}"
            return 1
        fi
    else
        echo -e "  ${RED}backend/.env not found${NC}"
        return 1
    fi
}

check_env "SUPABASE_URL"
check_env "SUPABASE_ANON_KEY"
check_env "SUPABASE_SERVICE_KEY"
check_env "DATABASE_URL"
check_env "OPENAI_API_KEY"

echo ""
echo "2️⃣ Checking GitHub Repository..."
echo ""

# Check if git remote exists
if git remote -v | grep -q "origin"; then
    REPO_URL=$(git remote get-url origin)
    echo -e "  Repository: ${GREEN}$REPO_URL${NC}"
    
    # Extract owner/repo from URL
    if [[ $REPO_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
        OWNER="${BASH_REMATCH[1]}"
        REPO="${BASH_REMATCH[2]}"
        echo -e "  GitHub: ${GREEN}$OWNER/$REPO${NC}"
        
        # Check if workflows exist
        if [ -d ".github/workflows" ]; then
            echo -e "  Workflows: ${GREEN}✓ Found${NC}"
            ls .github/workflows/*.yml | wc -l | xargs echo "    " workflows configured
        else
            echo -e "  Workflows: ${RED}✗ Not found${NC}"
        fi
    fi
else
    echo -e "  ${RED}No git remote configured${NC}"
fi

echo ""
echo "3️⃣ Checking Latest Commit..."
echo ""

# Show latest commit
git log -1 --pretty=format:"  Commit: %h%n  Author: %an%n  Date: %ad%n  Message: %s" --date=relative
echo ""

echo ""
echo "4️⃣ GitHub Actions Status..."
echo ""
echo "  Check your workflows at:"
echo "  https://github.com/$OWNER/$REPO/actions"
echo ""

echo "5️⃣ Quick Tests..."
echo ""

# Test if API is accessible (if deployed)
if [ -n "$DEPLOYED_API_URL" ]; then
    echo "  Testing deployed API at $DEPLOYED_API_URL..."
    if curl -s -f "$DEPLOYED_API_URL/health" > /dev/null; then
        echo -e "  API Health: ${GREEN}✓ Accessible${NC}"
    else
        echo -e "  API Health: ${RED}✗ Not accessible${NC}"
    fi
else
    echo -e "  ${YELLOW}DEPLOYED_API_URL not set - skipping API test${NC}"
fi

echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Check GitHub Actions: https://github.com/$OWNER/$REPO/actions"
echo "2. Monitor the deployment workflow"
echo "3. Once deployed, test your API endpoints"
echo "4. Check Supabase dashboard for database activity"
echo ""

# Check if USE_SUPABASE_AUTH is enabled
if grep -q "USE_SUPABASE_AUTH=true" backend/.env 2>/dev/null; then
    echo -e "✅ ${GREEN}Supabase authentication is ENABLED${NC}"
else
    echo -e "⚠️  ${YELLOW}Supabase authentication is DISABLED (using local JWT)${NC}"
fi

echo ""
echo "🚀 Deployment verification complete!"