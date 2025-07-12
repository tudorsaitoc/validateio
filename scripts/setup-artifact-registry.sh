#!/bin/bash

# This script sets up Google Artifact Registry for the project
# Run this once before deploying

PROJECT_ID=$1
REGION="us-central1"

if [ -z "$PROJECT_ID" ]; then
    echo "Usage: ./setup-artifact-registry.sh YOUR_PROJECT_ID"
    exit 1
fi

echo "Setting up Artifact Registry for project: $PROJECT_ID"

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable artifactregistry.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
gcloud services enable run.googleapis.com --project=$PROJECT_ID

# Create repository if it doesn't exist
echo "Creating Artifact Registry repository..."
gcloud artifacts repositories create cloud-run-source-deploy \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for ValidateIO" \
    --project=$PROJECT_ID || echo "Repository already exists"

echo "Setup complete!"
echo ""
echo "Make sure you have the following GitHub secrets configured:"
echo "- GCP_PROJECT_ID: $PROJECT_ID"
echo "- GCP_PROJECT_NUMBER: $(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')"
echo "- GCP_SA_KEY: Your service account JSON key"