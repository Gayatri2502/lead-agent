"""
GETTING STARTED GUIDE

Complete instructions to get the AI Voice Receptionist running locally.
"""

## 🚀 Quick Start (5 minutes)

### Prerequisites

```bash
# Check you have installed:
docker --version        # v24+
docker-compose --version # v2.10+
git --version           # any recent version
```

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai-voice-receptionist
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings (minimal config):
# - OPENAI_API_KEY=sk-... (from https://platform.openai.com/api-keys)
# - TWILIO_ACCOUNT_SID=... (from Twilio dashboard)
# - TWILIO_AUTH_TOKEN=...
# - TWILIO_PHONE_NUMBER=+1...
```

### 3. Start Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Verify services are running
docker-compose ps

# Wait for database to initialize (10-15 seconds)
sleep 15
```

### 4. Access Application

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Nginx Proxy**: http://localhost

### 5. First Login

1. Open http://localhost:3000
2. Register a new account
3. Login with credentials
4. Explore the dashboard

## 📋 Detailed Setup

### Step 1: System Requirements

**Minimum specs:**
- 4GB RAM
- 10GB free disk space
- Internet connection for APIs

**Required software:**
- Docker Engine 20.10+
- Docker Compose 2.10+
- Git

### Step 2: Clone & Configure

```bash
# 1. Clone with SSH
git clone git@github.com:your-org/ai-voice-receptionist.git
cd ai-voice-receptionist

# 2. Copy environment file
cp .env.example .env

# 3. Edit .env
vim .env  # or use your editor

# Essential variables:
DATABASE_URL=postgresql://user:password@postgres:5432/business_assistant
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=sk-your-key-here
TWILIO_ACCOUNT_SID=ACxxxxxx
TWILIO_AUTH_TOKEN=xxxxxx
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
SECRET_KEY=generate-random-secret-key
```

### Step 3: Create Environment File

**Important**: The following must be set:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Database
DATABASE_URL=postgresql://businessuser:secure_password@postgres:5432/business_assistant

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=$(openssl rand -hex 32)  # Generate random key

# OpenAI (https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-...

# Twilio (https://console.twilio.com)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=+1...

# Email (SMTP) - optional
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_NAME=AI Voice Receptionist
```

### Step 4: Start with Docker Compose

```bash
# Build images
docker-compose build

# Start all services in background
docker-compose up -d

# Check status
docker-compose ps
# Output should show: postgres, redis, backend, frontend, nginx all "Up"

# Watch logs
docker-compose logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Step 5: Initialize Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed sample data (optional)
docker-compose exec backend python -m app.database.seed

# Verify database
docker-compose exec postgres psql -U businessuser -d business_assistant -c "SELECT COUNT(*) FROM businesses;"
```

### Step 6: Verify Installation

```bash
# 1. Check backend health
curl http://localhost:8000/health
# Response: {"status": "healthy", "environment": "development"}

# 2. Check frontend
curl http://localhost:3000
# Response: HTML page

# 3. Check API documentation
curl http://localhost:8000/docs
# Response: Swagger UI

# 4. Access in browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Nginx: http://localhost
```

## 🔐 Initial Setup

### Create Admin User

```bash
# Access backend container
docker-compose exec backend bash

# Create admin user
python -c "
from app.database.db import SessionLocal
from app.models import User, Business
from app.utils.security import get_password_hash

db = SessionLocal()

# Create business
business = Business(
    name='My Business',
    business_type='Healthcare',
    timezone='America/New_York'
)
db.add(business)
db.flush()

# Create admin user
user = User(
    business_id=business.id,
    email='admin@example.com',
    username='admin',
    password=get_password_hash('AdminPassword123'),
    first_name='Admin',
    last_name='User',
    role='admin',
    is_active=True
)
db.add(user)
db.commit()
print('Admin created: admin@example.com / AdminPassword123')
"
```

### Configure API Keys

1. Go to http://localhost:3000/api-settings
2. Generate new API key
3. Use for webhooks and integrations

## 🧪 Testing Locally

### Test Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'

# Use returned token
TOKEN="eyJ..."
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/auth/me
```

### Create Test Appointment

```bash
TOKEN="your-token"
BUSINESS_ID=1

curl -X POST http://localhost:8000/api/v1/appointments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": '$BUSINESS_ID',
    "customer_id": 1,
    "staff_id": 1,
    "start_time": "2024-12-20T14:00:00",
    "service_id": 1,
    "notes": "Test appointment"
  }'
```

## 📱 Connect Twilio

### Setup Webhooks

1. Get your public URL (for testing, use ngrok):
   ```bash
   ngrok http 80
   # Note the URL: https://xxxx-xx-xx-xx-xxx.ngrok.io
   ```

2. In Twilio Console:
   - Go to Phone Numbers
   - Select your number
   - Set Voice Webhook to:
     ```
     https://your-domain.com/api/v1/webhooks/twilio/incoming-call
     ```

3. Test incoming call:
   - Call your Twilio number
   - Should be handled by AI agent

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Common issues:
# 1. Port already in use
docker-compose ps
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # Database

# 2. Out of memory
# Increase Docker resources in settings

# 3. Database connection error
docker-compose logs postgres
# Check DATABASE_URL is correct
```

### Database Issues

```bash
# Connect to database
docker-compose exec postgres psql -U businessuser -d business_assistant

# List tables
\dt

# Check users
SELECT * FROM users;

# Reset database (WARNING: deletes data)
docker-compose down -v  # Remove volumes
docker-compose up -d
```

### Frontend Not Loading

```bash
# Check frontend logs
docker-compose logs frontend

# Clear cache and rebuild
docker-compose down frontend
docker-compose build frontend
docker-compose up -d frontend

# Access logs
curl http://localhost:3000
```

### API Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Verify API is running
curl http://localhost:8000/health

# Check database connection
docker-compose logs postgres
```

### Twilio Webhook Not Working

```bash
# 1. Verify webhook is registered
# Check Twilio Console > Phone Numbers > Your Number

# 2. Test webhook locally with ngrok
ngrok http 80

# 3. Check logs
docker-compose logs backend
# Look for incoming webhook requests

# 4. Verify API key is set
grep TWILIO .env
```

## 📚 Next Steps

After successful setup:

1. **Configure Business Settings**
   - Go to http://localhost:3000/settings
   - Set business hours, services, etc.

2. **Add Staff/Providers**
   - Go to http://localhost:3000/staff
   - Add team members

3. **Create Services**
   - Add available services/treatments
   - Set duration and pricing

4. **Customize AI Agent**
   - Edit `backend/app/ai/conversation.py`
   - Adjust system prompt for your business

5. **Test End-to-End**
   - Make test call to your Twilio number
   - Verify appointment created
   - Check dashboard for analytics

6. **Deploy to Production**
   - Follow [DEPLOYMENT.md](docs/DEPLOYMENT.md)
   - Configure SSL certificates
   - Set up monitoring

## 📖 Documentation

- **[README.md](README.md)** - Project overview
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
- **[BACKEND.md](docs/BACKEND.md)** - Backend guide
- **[FRONTEND.md](docs/FRONTEND.md)** - Frontend guide
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment

## 🆘 Getting Help

### Check Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Follow logs
docker-compose logs -f backend
```

### Common Commands

```bash
# Stop all services
docker-compose down

# Start services
docker-compose up -d

# Restart a service
docker-compose restart backend

# Execute command in container
docker-compose exec backend bash

# Rebuild images
docker-compose build --no-cache

# Remove everything (WARNING: deletes data)
docker-compose down -v
```

### Database Commands

```bash
# Connect to database
docker-compose exec postgres psql -U businessuser -d business_assistant

# Backup database
docker-compose exec postgres pg_dump -U businessuser business_assistant > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres psql -U businessuser business_assistant
```

## ✅ Checklist

- [ ] Docker and Docker Compose installed
- [ ] Repository cloned
- [ ] .env file created and configured
- [ ] Services started: `docker-compose up -d`
- [ ] Database migrations run: `docker-compose exec backend alembic upgrade head`
- [ ] Frontend accessible: http://localhost:3000
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] Can register and login
- [ ] Twilio webhook configured (if testing calls)
- [ ] OpenAI API key verified
- [ ] Ready to develop!

## 🚀 You're Ready!

The application is fully running. Start developing or deploying to production.

Questions? Check the documentation or GitHub Issues.

Happy coding! 🎉
