#!/bin/bash

# Quick commands for development

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_step() {
    echo -e "${BLUE}➜${NC} $1"
}

echo_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Logs
if [ "$1" = "logs" ]; then
    echo_step "Showing logs..."
    docker-compose logs -f ${2:-}
    
# Database
elif [ "$1" = "db" ]; then
    echo_step "Connecting to database..."
    docker-compose exec postgres psql -U businessuser -d business_assistant
    
# Backend shell
elif [ "$1" = "backend-shell" ]; then
    echo_step "Opening backend shell..."
    docker-compose exec backend bash
    
# Frontend shell
elif [ "$1" = "frontend-shell" ]; then
    echo_step "Opening frontend shell..."
    docker-compose exec frontend bash
    
# Database backup
elif [ "$1" = "backup" ]; then
    echo_step "Backing up database..."
    docker-compose exec postgres pg_dump -U businessuser business_assistant > "backup_$(date +%s).sql"
    echo_success "Backup created"
    
# Database restore
elif [ "$1" = "restore" ]; then
    if [ -z "$2" ]; then
        echo "Usage: ./dev.sh restore <backup_file>"
        exit 1
    fi
    echo_step "Restoring database from $2..."
    cat "$2" | docker-compose exec -T postgres psql -U businessuser business_assistant
    echo_success "Database restored"
    
# Migrations
elif [ "$1" = "migrate" ]; then
    echo_step "Running database migrations..."
    docker-compose exec backend alembic upgrade head
    echo_success "Migrations complete"
    
# Clean
elif [ "$1" = "clean" ]; then
    echo_step "Cleaning up..."
    docker-compose down -v
    echo_success "Cleanup complete"
    
# Restart
elif [ "$1" = "restart" ]; then
    echo_step "Restarting services..."
    docker-compose restart ${2:-}
    echo_success "Services restarted"
    
# Install deps
elif [ "$1" = "install" ]; then
    echo_step "Installing dependencies..."
    if [ "$2" = "backend" ]; then
        pip install -r backend/requirements.txt
    elif [ "$2" = "frontend" ]; then
        cd frontend && npm install
    else
        pip install -r backend/requirements.txt
        cd frontend && npm install
    fi
    echo_success "Dependencies installed"
    
# Tests
elif [ "$1" = "test" ]; then
    echo_step "Running tests..."
    if [ "$2" = "backend" ]; then
        docker-compose exec backend pytest tests/ -v
    elif [ "$2" = "frontend" ]; then
        docker-compose exec frontend npm test
    else
        docker-compose exec backend pytest tests/ -v
        docker-compose exec frontend npm test
    fi
    
# API
elif [ "$1" = "api-docs" ]; then
    echo_step "Opening API docs..."
    open http://localhost:8000/docs || xdg-open http://localhost:8000/docs
    
# Frontend
elif [ "$1" = "frontend" ]; then
    echo_step "Opening frontend..."
    open http://localhost:3000 || xdg-open http://localhost:3000
    
# Health check
elif [ "$1" = "health" ]; then
    echo_step "Checking service health..."
    echo -n "Backend: "
    curl -s http://localhost:8000/health | jq '.status' || echo "❌ Down"
    echo -n "Frontend: "
    curl -s http://localhost:3000 > /dev/null && echo "✓ Running" || echo "❌ Down"
    
# Help
else
    echo "Available commands:"
    echo ""
    echo "  logs [service]           Show logs"
    echo "  db                       Connect to database"
    echo "  backend-shell            Open backend shell"
    echo "  frontend-shell           Open frontend shell"
    echo "  backup                   Backup database"
    echo "  restore <file>           Restore database"
    echo "  migrate                  Run migrations"
    echo "  clean                    Remove all containers/volumes"
    echo "  restart [service]        Restart services"
    echo "  install [service]        Install dependencies"
    echo "  test [backend|frontend]  Run tests"
    echo "  api-docs                 Open API documentation"
    echo "  frontend                 Open frontend dashboard"
    echo "  health                   Check service health"
    echo ""
fi
