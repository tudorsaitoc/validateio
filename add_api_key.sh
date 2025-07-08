#!/bin/bash

# Quick script to add OpenAI API key

echo "🔑 ValidateIO - Add OpenAI API Key"
echo "================================="
echo ""

# Check if backend/.env exists
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp .env.example backend/.env
fi

echo "Please enter your OpenAI API key:"
echo "(Get one at: https://platform.openai.com/api-keys)"
echo ""
read -p "OpenAI API Key (sk-...): " api_key

if [[ $api_key == sk-* ]]; then
    # Update or add the API key
    if grep -q "OPENAI_API_KEY=" backend/.env; then
        # On macOS, use -i '' for in-place editing
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" backend/.env
        else
            sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" backend/.env
        fi
    else
        echo "OPENAI_API_KEY=$api_key" >> backend/.env
    fi
    
    echo ""
    echo "✅ API key added successfully!"
    echo ""
    echo "You can now run:"
    echo "  cd backend && python test_validation_pipeline.py"
else
    echo ""
    echo "❌ Invalid API key format. OpenAI keys start with 'sk-'"
    echo "Please try again with a valid key."
fi