@echo off
REM Development helper script for Windows
REM Usage: dev.bat [command]

setlocal enabledelayedexpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="logs" goto logs
if "%1"=="db" goto db
if "%1"=="migrate" goto migrate
if "%1"=="test" goto test
if "%1"=="clean" goto clean
if "%1"=="health" goto health
if "%1"=="api-docs" goto apidocs
if "%1"=="frontend" goto frontend

goto help

:logs
docker-compose logs -f %2
goto :eof

:db
docker-compose exec postgres psql -U businessuser -d business_assistant
goto :eof

:migrate
echo Running migrations...
docker-compose exec -T backend alembic upgrade head
echo ✓ Migrations complete
goto :eof

:test
if "%2"=="backend" (
    docker-compose exec backend pytest tests/ -v
) else if "%2"=="frontend" (
    docker-compose exec frontend npm test
) else (
    docker-compose exec backend pytest tests/ -v
    docker-compose exec frontend npm test
)
goto :eof

:clean
echo Cleaning up...
docker-compose down -v
echo ✓ Cleanup complete
goto :eof

:health
echo Checking service health...
echo Backend: 
curl http://localhost:8000/health
echo Frontend: 
curl http://localhost:3000 > nul && echo ✓ Running || echo ❌ Down
goto :eof

:apidocs
start http://localhost:8000/docs
goto :eof

:frontend
start http://localhost:3000
goto :eof

:help
echo Available commands:
echo.
echo   logs [service]     - Show logs
echo   db                 - Connect to database
echo   migrate            - Run migrations
echo   test [backend]     - Run tests
echo   clean              - Remove all containers/volumes
echo   health             - Check service health
echo   api-docs           - Open API documentation
echo   frontend           - Open frontend dashboard
echo.
