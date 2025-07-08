#!/bin/bash

echo "🔧 Update Existing Cloud Run Service"
echo "==================================="
echo ""

echo "Since the service already exists, let's update it!"
echo ""

echo "Run these commands in Google Cloud Shell:"
echo "https://console.cloud.google.com/cloudshell"
echo ""

cat << 'COMMANDS'
# Set variables
PROJECT_ID=validateio
REGION=us-central1
SERVICE_NAME=validateio-backend

# First, let's check the current service
echo "Current service status:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

# Option 1: Delete and recreate (if you want a fresh start)
echo "To delete and recreate:"
echo "gcloud run services delete $SERVICE_NAME --region=$REGION"

# Option 2: Update the existing service with a new image
echo "Building and deploying from source..."
cd /tmp
git clone https://github.com/tudorsaitoc/validateio.git
cd validateio/backend

# Deploy directly from source (Cloud Build will handle everything)
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region=$REGION \
  --allow-unauthenticated \
  --set-env-vars="ENVIRONMENT=production" \
  --min-instances=0 \
  --max-instances=10

# Get the URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo "Service URL: $SERVICE_URL"

# Test it
curl "$SERVICE_URL/health"
COMMANDS

echo ""
echo "Alternative: Quick fix via Console"
echo "1. Go to: https://console.cloud.google.com/run/detail/$REGION/validateio-backend/revisions"
echo "2. Click 'EDIT & DEPLOY NEW REVISION'"
echo "3. Update environment variables"
echo "4. Click 'DEPLOY'"