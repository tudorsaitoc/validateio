#!/bin/bash

# Setup local development to work with deployed services
echo "🔧 Setup Local Development with Cloud Services"
echo "============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "This script will configure your local environment to work with:"
echo "- Supabase (Database & Auth)"
echo "- Deployed Backend (optional)"
echo "- Local development server"
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "Creating backend/.env..."
    cp backend/.env.example backend/.env 2>/dev/null || touch backend/.env
fi

# Function to update .env
update_env() {
    local key=$1
    local value=$2
    if grep -q "^$key=" backend/.env; then
        sed -i.bak "s|^$key=.*|$key=$value|" backend/.env
    else
        echo "$key=$value" >> backend/.env
    fi
}

# 1. Configure for local development with Supabase
echo "1️⃣ Local Development Mode"
echo ""
echo "Your backend/.env already has Supabase configured."
echo "Let's verify the settings..."
echo ""

# Show current Supabase config
echo "Current Supabase Configuration:"
grep "SUPABASE_" backend/.env | grep -v "^#"
echo ""

# 2. Optional: Use deployed backend
echo "2️⃣ Connect Frontend to Deployed Backend (Optional)"
echo ""
read -p "Do you want to use the deployed backend API? (y/n) [n]: " use_deployed

if [[ $use_deployed =~ ^[Yy]$ ]]; then
    read -p "Enter your Cloud Run backend URL: " backend_url
    if [ ! -z "$backend_url" ]; then
        # Update frontend .env.local
        echo "NEXT_PUBLIC_API_URL=$backend_url" > frontend/.env.local
        echo "NEXT_PUBLIC_SUPABASE_URL=$(grep SUPABASE_URL backend/.env | cut -d= -f2)" >> frontend/.env.local
        echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=$(grep SUPABASE_ANON_KEY backend/.env | cut -d= -f2)" >> frontend/.env.local
        echo -e "${GREEN}✅ Frontend configured to use deployed backend${NC}"
    fi
else
    # Local backend
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
    echo "NEXT_PUBLIC_SUPABASE_URL=$(grep SUPABASE_URL backend/.env | cut -d= -f2)" >> frontend/.env.local
    echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=$(grep SUPABASE_ANON_KEY backend/.env | cut -d= -f2)" >> frontend/.env.local
    echo -e "${GREEN}✅ Frontend configured for local development${NC}"
fi

# 3. Start local development
echo ""
echo "3️⃣ Starting Local Development"
echo ""
echo "Choose your development mode:"
echo "1) Full stack (Frontend + Backend + Supabase)"
echo "2) Frontend only (using deployed backend)"
echo "3) Backend only (API development)"
echo ""
read -p "Select mode [1]: " dev_mode
dev_mode=${dev_mode:-1}

case $dev_mode in
    1)
        cat > start_dev.sh << 'EOF'
#!/bin/bash
echo "Starting ValidateIO Full Stack Development..."

# Start backend
echo "Starting backend..."
cd backend
source .venv/bin/activate 2>/dev/null || python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🚀 Development servers running:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait and handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID" INT
wait
EOF
        ;;
    2)
        cat > start_dev.sh << 'EOF'
#!/bin/bash
echo "Starting Frontend Development..."
cd frontend
npm install
npm run dev
EOF
        ;;
    3)
        cat > start_dev.sh << 'EOF'
#!/bin/bash
echo "Starting Backend Development..."
cd backend
source .venv/bin/activate 2>/dev/null || python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
EOF
        ;;
esac

chmod +x start_dev.sh
echo -e "${GREEN}✅ Created start_dev.sh${NC}"

echo ""
echo "📋 Summary:"
echo "- Supabase: Configured"
echo "- Frontend: $(grep NEXT_PUBLIC_API_URL frontend/.env.local | cut -d= -f2)"
echo "- Development script: ./start_dev.sh"
echo ""
echo "🎯 Next Steps:"
echo "1. Run: ./start_dev.sh"
echo "2. Open: http://localhost:3000 (frontend)"
echo "3. Test: http://localhost:8000/docs (backend API)"
echo "4. Create your first validation!"