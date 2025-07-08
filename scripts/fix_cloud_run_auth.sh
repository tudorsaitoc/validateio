#!/bin/bash

# Script to fix Cloud Run authentication issues

echo "🔧 Fixing Cloud Run Authentication"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "This script will help fix the 403 Forbidden error on Cloud Run."
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "1️⃣ Making Cloud Run service publicly accessible..."
echo ""

read -p "Enter your Cloud Run service name [validateio-backend]: " SERVICE_NAME
SERVICE_NAME=${SERVICE_NAME:-validateio-backend}

read -p "Enter your GCP region [us-central1]: " REGION
REGION=${REGION:-us-central1}

echo ""
echo "Running: gcloud run services add-iam-policy-binding $SERVICE_NAME \\"
echo "  --member=\"allUsers\" \\"
echo "  --role=\"roles/run.invoker\" \\"
echo "  --region=$REGION"
echo ""

# Make the service public
gcloud run services add-iam-policy-binding $SERVICE_NAME \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=$REGION

echo ""
echo -e "${GREEN}✅ Service should now be publicly accessible!${NC}"
echo ""

# Get the service URL
echo "2️⃣ Getting service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

if [ ! -z "$SERVICE_URL" ]; then
    echo -e "Service URL: ${GREEN}$SERVICE_URL${NC}"
    echo ""
    
    echo "3️⃣ Testing health endpoint..."
    if curl -s -f "$SERVICE_URL/health" > /dev/null; then
        echo -e "${GREEN}✅ Health endpoint is accessible!${NC}"
        echo ""
        echo "Response:"
        curl -s "$SERVICE_URL/health" | python3 -m json.tool
    else
        echo "❌ Health endpoint still not accessible"
        echo ""
        echo "Troubleshooting:"
        echo "1. Check Cloud Run logs:"
        echo "   gcloud run services logs read $SERVICE_NAME --region=$REGION"
        echo ""
        echo "2. Check if the service is running:"
        echo "   gcloud run services describe $SERVICE_NAME --region=$REGION"
    fi
else
    echo "❌ Could not get service URL"
fi

echo ""
echo "📝 Alternative Solutions:"
echo ""
echo "1. If you want to keep authentication but allow health checks:"
echo "   - Update your Cloud Run service to use --allow-unauthenticated flag"
echo "   - Or implement custom authentication middleware that excludes /health"
echo ""
echo "2. Update via Console:"
echo "   - Go to https://console.cloud.google.com/run"
echo "   - Click on your service"
echo "   - Click 'EDIT & DEPLOY NEW REVISION'"
echo "   - Under 'Authentication', select 'Allow unauthenticated invocations'"
echo "   - Click 'DEPLOY'"
echo ""
echo "3. Redeploy with public access:"
echo "   gcloud run deploy $SERVICE_NAME \\"
echo "     --image=IMAGE_URL \\"
echo "     --allow-unauthenticated \\"
echo "     --region=$REGION"