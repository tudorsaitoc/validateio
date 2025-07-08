#!/bin/bash

echo "🔍 Deployment Debugging Guide"
echo "============================"
echo ""

echo "1️⃣ Check GitHub Actions:"
echo "Go to: https://github.com/tudorsaitoc/validateio/actions"
echo ""
echo "Look for:"
echo "- Which workflow is failing? (CI or CD)"
echo "- Which step is failing?"
echo "- What's the error message?"
echo ""

echo "2️⃣ Common Issues & Solutions:"
echo ""

echo "❌ Error: 'Cannot find module'"
echo "✅ Fix: Missing dependencies in requirements.txt or package.json"
echo ""

echo "❌ Error: 'Invalid credentials' or 'Permission denied'"
echo "✅ Fix: GCP_SA_KEY might be incorrect or missing permissions"
echo ""

echo "❌ Error: 'Failed to build Docker image'"
echo "✅ Fix: Check Dockerfile.prod exists in backend/"
echo ""

echo "❌ Error: 'Artifact Registry not found'"
echo "✅ Fix: Enable Artifact Registry API in GCP Console"
echo ""

echo "3️⃣ Quick Checks:"
echo ""

# Check if Dockerfile exists
if [ -f backend/Dockerfile.prod ]; then
    echo "✅ backend/Dockerfile.prod exists"
else
    echo "❌ backend/Dockerfile.prod is missing!"
    echo "   Creating one now..."
    
    cat > backend/Dockerfile.prod << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
    echo "   Created backend/Dockerfile.prod"
fi

echo ""
echo "4️⃣ GCP Project Setup:"
echo ""
echo "Make sure these APIs are enabled in your GCP project:"
echo "1. Cloud Run API"
echo "2. Artifact Registry API"
echo "3. Cloud Build API"
echo ""
echo "Enable them at: https://console.cloud.google.com/apis/library"
echo ""

echo "5️⃣ Test Your Secrets Locally:"
cat << 'SCRIPT'

# Test if your secrets work
python3 << EOF
import base64
import json

# Test GCP_SA_KEY format
gcp_key = '''YOUR_GCP_SA_KEY_HERE'''
try:
    key_data = json.loads(gcp_key)
    print("✅ GCP_SA_KEY is valid JSON")
    print(f"   Project ID: {key_data.get('project_id')}")
    print(f"   Client Email: {key_data.get('client_email')}")
except:
    print("❌ GCP_SA_KEY is not valid JSON")

# Test Supabase connection
import os
print("\n✅ Supabase URL:", os.getenv('SUPABASE_URL', 'Not set'))
EOF

SCRIPT

echo ""
echo "6️⃣ Manual Deployment Test:"
echo ""
echo "If GitHub Actions keeps failing, try manual deployment:"
echo ""
echo "# Build locally"
echo "cd backend"
echo "docker build -t validateio-backend -f Dockerfile.prod ."
echo ""
echo "# Run locally with production settings"
echo "docker run -p 8000:8000 \\"
echo "  -e DATABASE_URL='your-supabase-url' \\"
echo "  -e SUPABASE_URL='your-supabase-url' \\"
echo "  -e OPENAI_API_KEY='your-key' \\"
echo "  validateio-backend"
echo ""

echo "Share the error message from GitHub Actions and I can help debug!"