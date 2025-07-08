#!/bin/bash

echo "🔍 GCP Setup Diagnostic"
echo "======================"
echo ""

echo "This script will help identify what's wrong with your GCP setup."
echo ""

echo "1️⃣ First, let's check if you have the right APIs enabled:"
echo ""
echo "Go to: https://console.cloud.google.com/apis/library"
echo "Make sure these are ENABLED:"
echo "- ✅ Cloud Run API"
echo "- ✅ Artifact Registry API" 
echo "- ✅ Cloud Build API"
echo "- ✅ Compute Engine API"
echo ""

echo "2️⃣ Check your Artifact Registry:"
echo ""
echo "Go to: https://console.cloud.google.com/artifacts"
echo "You need to create a repository named 'validateio' if it doesn't exist:"
echo ""
echo "Click '+ CREATE REPOSITORY' with these settings:"
echo "- Name: validateio"
echo "- Format: Docker"
echo "- Mode: Standard"
echo "- Region: us-central1 (or your region)"
echo ""

echo "3️⃣ Service Account Permissions:"
echo ""
echo "Your service account needs these roles:"
echo "- Artifact Registry Writer"
echo "- Cloud Run Admin"
echo "- Service Account User"
echo "- Storage Admin"
echo ""

echo "4️⃣ Quick Manual Test:"
echo ""
echo "If you have gcloud installed locally, try:"
echo ""
echo "# Test authentication"
echo "gcloud auth activate-service-account --key-file=path/to/your-key.json"
echo ""
echo "# List artifact repositories"
echo "gcloud artifacts repositories list --location=us-central1"
echo ""

echo "5️⃣ Alternative: Simple Cloud Run Deployment"
echo ""
echo "Instead of Artifact Registry, we can deploy directly from source:"
cat > .github/workflows/cd-simple.yml << 'EOF'
name: Simple CD

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v2
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}
    
    - name: Deploy to Cloud Run directly from source
      uses: google-github-actions/deploy-cloudrun@v2
      with:
        service: validateio-backend
        source: ./backend
        region: ${{ secrets.GCP_REGION }}
        env_vars: |
          DATABASE_URL=${{ secrets.DATABASE_URL }}
          SUPABASE_URL=${{ secrets.SUPABASE_URL }}
          SUPABASE_ANON_KEY=${{ secrets.SUPABASE_ANON_KEY }}
          OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          JWT_SECRET_KEY=${{ secrets.JWT_SECRET_KEY }}
          ENVIRONMENT=production
        flags: --allow-unauthenticated
EOF

echo ""
echo "Created: .github/workflows/cd-simple.yml"
echo ""
echo "This simpler workflow:"
echo "- Doesn't require Artifact Registry"
echo "- Builds directly on Cloud Run"
echo "- Fewer things to go wrong!"
echo ""

echo "6️⃣ Debugging Your Current Error:"
echo ""
echo "Please share the exact error from GitHub Actions, especially:"
echo "- Which step is failing?"
echo "- What's the error message?"
echo "- Is it authentication, permissions, or missing resources?"