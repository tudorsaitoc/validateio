#!/bin/bash

# Script to help set up Supabase environment variables

echo "🔧 Supabase Environment Setup"
echo "============================"
echo ""
echo "This script will help you add Supabase credentials to your backend/.env file."
echo ""
echo "You can find these values in your Supabase dashboard:"
echo "1. Go to https://app.supabase.com/project/YOUR_PROJECT/settings/api"
echo "2. Copy the values for URL, anon key, and service role key"
echo ""

# Function to append to .env if not exists
add_to_env() {
    local key=$1
    local prompt=$2
    
    if grep -q "^$key=" backend/.env 2>/dev/null; then
        echo "✓ $key already exists in backend/.env"
    else
        echo ""
        echo "$prompt"
        read -p "$key: " value
        if [ ! -z "$value" ]; then
            echo "$key=$value" >> backend/.env
            echo "✓ Added $key to backend/.env"
        fi
    fi
}

# Ensure backend/.env exists
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env 2>/dev/null || cp .env.example backend/.env
fi

# Add Supabase variables
add_to_env "SUPABASE_URL" "Enter your Supabase URL (e.g., https://xxxxx.supabase.co):"
add_to_env "SUPABASE_ANON_KEY" "Enter your Supabase anon/public key:"
add_to_env "SUPABASE_SERVICE_KEY" "Enter your Supabase service role key:"

# Ask about enabling Supabase auth
echo ""
read -p "Enable Supabase authentication? (y/n) [n]: " enable_auth
if [[ $enable_auth =~ ^[Yy]$ ]]; then
    if grep -q "^USE_SUPABASE_AUTH=" backend/.env; then
        sed -i.bak 's/USE_SUPABASE_AUTH=.*/USE_SUPABASE_AUTH=true/' backend/.env
    else
        echo "USE_SUPABASE_AUTH=true" >> backend/.env
    fi
    echo "✓ Enabled Supabase authentication"
fi

# Update DATABASE_URL for Supabase
echo ""
echo "Updating DATABASE_URL for Supabase..."
if [ ! -z "$SUPABASE_URL" ]; then
    # Extract project ID from URL
    if [[ $SUPABASE_URL =~ https://([^.]+)\.supabase\.co ]]; then
        PROJECT_ID="${BASH_REMATCH[1]}"
        DB_URL="postgresql://postgres.[PROJECT_ID]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres"
        echo ""
        echo "Your Supabase database URL format:"
        echo "$DB_URL"
        echo ""
        echo "You can find the exact URL in:"
        echo "Supabase Dashboard > Settings > Database > Connection string"
        echo ""
        read -p "Enter your Supabase DATABASE_URL: " db_url
        if [ ! -z "$db_url" ]; then
            if grep -q "^DATABASE_URL=" backend/.env; then
                sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=$db_url|" backend/.env
            else
                echo "DATABASE_URL=$db_url" >> backend/.env
            fi
            echo "✓ Updated DATABASE_URL"
        fi
    fi
fi

echo ""
echo "✅ Supabase environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run the migration in Supabase SQL editor:"
echo "   cat backend/supabase/migrations/20250108_initial_schema.sql"
echo ""
echo "2. Test the connection:"
echo "   python3 scripts/test_supabase_connection.py"
echo ""
echo "3. Start the development server:"
echo "   cd backend && uvicorn main:app --reload"