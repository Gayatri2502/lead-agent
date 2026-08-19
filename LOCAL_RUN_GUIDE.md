"""
Quick start guide for running the project locally without Docker
"""

# ============================================
# QUICK START - LOCAL STREAMLIT DEMO (No Docker Needed)
# ============================================

## STEP 1: Install Python
# Download Python 3.11 from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation


## STEP 2: Install Streamlit and Dependencies
# Open PowerShell and run:

pip install -r streamlit_requirements.txt


## STEP 3: Run the Streamlit Application
# In PowerShell, from the project directory:

streamlit run app.py

# This will:
# - Start the Streamlit development server
# - Open http://localhost:8501 in your browser
# - Show a live dashboard with sample data


## STEP 4: Explore the Dashboard
# - Navigate through all pages using the sidebar
# - View dashboard, appointments, customers, calls
# - Check analytics and settings
# - All data is sample/demo data for now


# ============================================
# RUNNING THE FULL BACKEND (Optional - Requires Python 3.11+)
# ============================================

## If you want to also run the FastAPI backend:

# 1. Create a Python virtual environment:
python -m venv backend_env

# 2. Activate it:
# On Windows:
.\backend_env\Scripts\activate

# 3. Install backend dependencies:
pip install -r backend/requirements.txt

# 4. Run the backend:
python -m uvicorn backend.app.main:app --reload

# Backend will run at http://localhost:8000
# API docs at http://localhost:8000/docs


# ============================================
# RUNNING FRONTEND (Optional - Requires Node.js)
# ============================================

## If you want to run the Next.js frontend:

# 1. Install Node.js from https://nodejs.org/ (LTS version)

# 2. Navigate to frontend directory:
cd frontend

# 3. Install dependencies:
npm install

# 4. Start development server:
npm run dev

# Frontend will run at http://localhost:3000


# ============================================
# ALL THREE RUNNING TOGETHER
# ============================================

## Terminal 1 - Streamlit Dashboard:
streamlit run app.py
# Access at http://localhost:8501

## Terminal 2 - FastAPI Backend:
python -m uvicorn backend.app.main:app --reload
# Access at http://localhost:8000/docs

## Terminal 3 - Next.js Frontend:
cd frontend && npm run dev
# Access at http://localhost:3000


# ============================================
# COMMANDS REFERENCE
# ============================================

# Check Python version:
python --version

# Create virtual environment:
python -m venv venv_name

# Activate virtual environment:
.\venv_name\Scripts\activate

# Install packages:
pip install -r requirements.txt

# Run Streamlit:
streamlit run app.py

# Run FastAPI:
python -m uvicorn backend.app.main:app --reload

# Run Next.js:
npm run dev

# Stop any running server:
# Press Ctrl + C in the terminal


# ============================================
# TROUBLESHOOTING
# ============================================

# If "streamlit: command not found":
# - Make sure you ran: pip install -r streamlit_requirements.txt
# - Make sure you activated virtual environment (if using one)

# If port 8501 is already in use:
streamlit run app.py --server.port 8502

# If you want to clear all Python cache:
Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force

# For more Streamlit options:
streamlit --help
