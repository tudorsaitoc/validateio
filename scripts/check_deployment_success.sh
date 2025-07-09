#!/bin/bash

echo "🎉 Checking ValidateIO Deployment"
echo "================================="
echo ""

# Your Cloud Run service should be at one of these URLs:
echo "Possible service URLs:"
echo "1. https://validateio-backend-847973892251.us-central1.run.app"
echo "2. https://validateio-backend-validateio.us-central1.run.app"
echo "3. Check the GitHub Actions logs for the exact URL"
echo ""

# Test the original URL you provided
echo "Testing your service..."
URL="https://validateio-847973892251.us-central1.run.app"

echo "Checking: $URL/health"
if curl -s "$URL/health" | python3 -m json.tool; then
    echo ""
    echo "✅ Your service is running!"
else
    echo ""
    echo "This URL might not be correct. Check GitHub Actions logs for the actual URL."
fi

echo ""
echo "To find your service URL:"
echo "1. Go to: https://console.cloud.google.com/run?project=validateio"
echo "2. Click on 'validateio-backend'"
echo "3. Copy the URL shown at the top"
echo ""
echo "Or check the GitHub Actions logs:"
echo "1. Go to: https://github.com/tudorsaitoc/validateio/actions"
echo "2. Click on the successful 'Diagnostic CD' workflow"
echo "3. Look for 'Service deployed to:' in the logs"