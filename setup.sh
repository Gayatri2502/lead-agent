#!/bin/bash

# AI Voice Receptionist - Quick Start Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "🚀 AI Voice Receptionist - Quick Start Setup"
echo "==========================================="

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git."
    exit 1
fi

echo "✅ All prerequisites met"

# Create .env file
echo ""
echo "Setting up environment..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - TWILIO_ACCOUNT_SID"
    echo "   - TWILIO_AUTH_TOKEN"
    echo "   - TWILIO_PHONE_NUMBER"
else
    echo "✅ .env file already exists"
fi

# Build and start services
echo ""
echo "Building and starting services..."
echo "This may take a few minutes on first run..."

docker-compose build
docker-compose up -d

echo "✅ Services started"

# Wait for database to be ready
echo ""
echo "Waiting for database to initialize..."
sleep 15

# Run migrations
echo ""
echo "Running database migrations..."
docker-compose exec -T backend alembic upgrade head
echo "✅ Migrations completed"

# Summary
echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo "==========================================="
echo ""
echo "Services are now running:"
echo "  • Frontend: http://localhost:3000"
echo "  • Backend API: http://localhost:8000"
echo "  • API Documentation: http://localhost:8000/docs"
echo "  • Nginx Proxy: http://localhost"
echo ""
echo "Database: PostgreSQL at postgres:5432"
echo "Cache: Redis at redis:6379"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Register a new account"
echo "  3. Login and explore the dashboard"
echo "  4. Configure your Twilio webhook for incoming calls"
echo ""
echo "For detailed setup instructions, see GETTING_STARTED.md"
echo "For troubleshooting, check the documentation in /docs"
echo ""
