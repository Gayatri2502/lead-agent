@echo off
REM AI Voice Receptionist - Local Streamlit Quick Start
REM No Docker, No Phone Number Required - Just Pure Python!

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🤖 AI Voice Receptionist - Local Demo
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please download Python 3.11+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo Then restart PowerShell and try again.
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    pause
    exit /b 1
)

echo ✅ pip is available
echo.

REM Install dependencies
echo Installing Streamlit and dependencies...
echo This may take a minute on first run...
echo.

pip install -r streamlit_requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.

REM Start Streamlit
echo ========================================
echo Starting Streamlit Dashboard...
echo ========================================
echo.
echo 🚀 Opening dashboard at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

python -m streamlit run app.py --logger.level=info

pause
