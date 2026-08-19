@echo off
REM AI Voice Receptionist - Quick Start Script (Windows)
REM This script sets up the entire development environment

setlocal enabledelayedexpansion

echo ========================================
echo 🚀 AI Voice Receptionist - Quick Start Setup
echo ========================================
echo.

REM Check prerequisites
echo Checking prerequisites...

docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop for Windows.
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Desktop for Windows.
    exit /b 1
)

echo ✅ All prerequisites met
echo.

REM Create .env file
echo Setting up environment...

if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file
    echo.
    echo ⚠️  Please edit .env and add your API keys:
    echo    - OPENAI_API_KEY
    echo    - TWILIO_ACCOUNT_SID
    echo    - TWILIO_AUTH_TOKEN
    echo    - TWILIO_PHONE_NUMBER
    echo.
    start notepad .env
) else (
    echo ✅ .env file already exists
)

REM Build and start services
echo.
echo Building and starting services...
echo This may take a few minutes on first run...
echo.

docker-compose build
docker-compose up -d

echo ✅ Services started
echo.

REM Wait for database to be ready
echo Waiting for database to initialize...
timeout /t 15 /nobreak

REM Run migrations
echo.
echo Running database migrations...
docker-compose exec -T backend alembic upgrade head
echo ✅ Migrations completed
echo.

REM Summary
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Services are now running:
echo   • Frontend: http://localhost:3000
echo   • Backend API: http://localhost:8000
echo   • API Documentation: http://localhost:8000/docs
echo   • Nginx Proxy: http://localhost
echo.
echo Database: PostgreSQL at postgres:5432
echo Cache: Redis at redis:6379
echo.
echo Next steps:
echo   1. Open http://localhost:3000 in your browser
echo   2. Register a new account
echo   3. Login and explore the dashboard
echo   4. Configure your Twilio webhook for incoming calls
echo.
echo For detailed setup instructions, see GETTING_STARTED.md
echo For troubleshooting, check the documentation in /docs
echo.
pause
