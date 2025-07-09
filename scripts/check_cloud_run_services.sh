#!/bin/bash

echo "🔍 Checking Cloud Run Services"
echo "============================="
echo ""
echo "Run these commands in Google Cloud Shell:"
echo "https://console.cloud.google.com/cloudshell"
echo ""

cat << 'COMMANDS'
# Set your project
gcloud config set project validateio

# List all Cloud Run services
echo "Existing Cloud Run services:"
gcloud run services list --platform=managed

# Check the specific service
echo ""
echo "Details for validateio-backend service:"
gcloud run services describe validateio-backend --region=us-central1 --platform=managed

# Get the service URL
SERVICE_URL=$(gcloud run services describe validateio-backend --region=us-central1 --format="value(status.url)")
echo ""
echo "Current service URL: $SERVICE_URL"

# Test the health endpoint
echo ""
echo "Testing current deployment:"
curl "$SERVICE_URL/health" || echo "Health check failed"
COMMANDS

echo ""
echo "📝 What's happening:"
echo "- Your GCP project is named: validateio ✅"
echo "- The Cloud Run service is named: validateio-backend"
echo "- The error occurs because this service already exists"
echo ""
echo "🔧 Solutions:"
echo ""
echo "1. Delete the existing service and redeploy:"
echo "   gcloud run services delete validateio-backend --region=us-central1"
echo ""
echo "2. Or manually update it in the Console:"
echo "   https://console.cloud.google.com/run/detail/us-central1/validateio-backend/revisions?project=validateio"