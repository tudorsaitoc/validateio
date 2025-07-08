#!/bin/bash

# Script to help check deployment status and logs
echo "🔍 Deployment Status Check"
echo "========================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "1️⃣ GitHub Actions Status"
echo "Check your latest workflow runs at:"
echo -e "${GREEN}https://github.com/tudorsaitoc/validateio/actions${NC}"
echo ""

echo "2️⃣ Required GitHub Secrets"
echo "Add missing secrets at:"
echo -e "${GREEN}https://github.com/tudorsaitoc/validateio/settings/secrets/actions${NC}"
echo ""

echo "Required secrets for deployment:"
echo "- GCP_PROJECT_ID (your Google Cloud project ID)"
echo "- GCP_REGION (e.g., us-central1)"
echo "- GCP_SA_KEY (service account JSON key)"
echo "- DATABASE_URL (Supabase PostgreSQL connection string)"
echo "- SUPABASE_URL (your Supabase project URL)"
echo "- SUPABASE_ANON_KEY (Supabase anonymous key)"
echo "- OPENAI_API_KEY (for AI agents)"
echo ""

echo "3️⃣ Cloud Run Service Status"
echo "Check your Cloud Run service at:"
echo -e "${GREEN}https://console.cloud.google.com/run/detail/us-central1/validateio-backend/metrics${NC}"
echo ""

echo "4️⃣ Common Issues & Fixes"
echo ""
echo "Issue: 'Placeholder' page showing"
echo "Fix: Deployment hasn't completed. Check GitHub Actions for errors."
echo ""
echo "Issue: Authentication failed"
echo "Fix: GCP_SA_KEY might be invalid or missing permissions."
echo ""
echo "Issue: Build failed"
echo "Fix: Check Dockerfile or missing dependencies."
echo ""

echo "5️⃣ Quick Fixes"
echo ""
echo "To manually test secrets locally:"
cat << 'EOF'

# Test Supabase connection
python3 << PYTHON
import os
from dotenv import load_dotenv
load_dotenv('backend/.env')

print("SUPABASE_URL:", "SET" if os.getenv("SUPABASE_URL") else "NOT SET")
print("SUPABASE_ANON_KEY:", "SET" if os.getenv("SUPABASE_ANON_KEY") else "NOT SET")
print("OPENAI_API_KEY:", "SET" if os.getenv("OPENAI_API_KEY") else "NOT SET")
PYTHON

EOF

echo ""
echo "6️⃣ Get Help"
echo "- Check build logs in GitHub Actions"
echo "- View Cloud Run logs in GCP Console"
echo "- Review error messages for missing secrets"
echo ""
echo "Run the test-secrets workflow to check which secrets are missing!"