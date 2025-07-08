#!/bin/bash

# Docker installation helper script

echo "🐳 Docker Installation Guide"
echo "=========================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 macOS detected"
    echo ""
    echo "Option 1: Install Docker Desktop (Recommended)"
    echo "  1. Download from: https://www.docker.com/products/docker-desktop/"
    echo "  2. Open the .dmg file and drag Docker to Applications"
    echo "  3. Start Docker Desktop from Applications"
    echo ""
    echo "Option 2: Install via Homebrew"
    echo "  brew install --cask docker"
    echo ""
    echo "After installation:"
    echo "  1. Start Docker Desktop"
    echo "  2. Wait for Docker to fully start (icon in menu bar)"
    echo "  3. Run: ./scripts/dev.sh"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Linux detected"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install docker.io docker-compose"
    echo "  sudo usermod -aG docker $USER"
    echo "  # Log out and back in for group changes"
    echo ""
    echo "Fedora/RHEL/CentOS:"
    echo "  sudo dnf install docker docker-compose"
    echo "  sudo systemctl start docker"
    echo "  sudo systemctl enable docker"
    echo "  sudo usermod -aG docker $USER"
    echo ""
    echo "After installation:"
    echo "  1. Log out and log back in"
    echo "  2. Run: ./scripts/dev.sh"
    
else
    echo "❓ Unknown OS: $OSTYPE"
    echo "Please visit: https://docs.docker.com/get-docker/"
fi

echo ""
echo "🔍 To verify Docker installation:"
echo "  docker --version"
echo "  docker-compose --version"
echo ""
echo "💡 Alternative: Use local development mode"
echo "  ./scripts/dev_local.sh"
echo "  (Requires local PostgreSQL and Redis)"