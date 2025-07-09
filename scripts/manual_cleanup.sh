#!/bin/bash

echo "🧹 Manual Cloud Run Cleanup"
echo "=========================="
echo ""
echo "Run these commands in Google Cloud Shell:"
echo "https://shell.cloud.google.com/"
echo ""

cat << 'SCRIPT'
# Set project and region
export PROJECT_ID=validateio
export REGION=us-central1

gcloud config set project $PROJECT_ID

# List all Cloud Run services
echo "Current Cloud Run services:"
gcloud run services list --region=$REGION

# Delete the problematic service
echo ""
echo "Deleting validateio-backend..."
gcloud run services delete validateio-backend --region=$REGION --quiet

# Verify it's gone
echo ""
echo "Verifying deletion..."
sleep 5
if gcloud run services describe validateio-backend --region=$REGION 2>/dev/null; then
    echo "❌ Service still exists!"
    echo "Try deleting from Console: https://console.cloud.google.com/run"
else
    echo "✅ Service successfully deleted!"
fi

# Also check all regions in case it exists elsewhere
echo ""
echo "Checking other regions..."
for region in us-central1 us-east1 us-west1 europe-west1; do
    echo "Checking $region..."
    gcloud run services list --region=$region --filter="name:validateio-backend"
done
SCRIPT

echo ""
echo "Alternative: Delete via Console"
echo "1. Go to: https://console.cloud.google.com/run?project=validateio"
echo "2. Look for 'validateio-backend' in ALL regions"
echo "3. Select it and click DELETE"
echo "4. Wait for deletion to complete"
echo "5. Re-run the GitHub Actions workflow"