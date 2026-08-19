# AI Voice Receptionist - Production-Ready Application

A complete, enterprise-grade SaaS application for AI-powered voice receptionist and appointment booking system. Built with Next.js, FastAPI, PostgreSQL, and integrated with OpenAI and Twilio.

## 🎯 Features

### Core Features
- **AI Voice Reception**: Intelligent call handling with natural conversation
- **Appointment Booking**: Automated scheduling and calendar management
- **Customer Management**: Complete customer profile and interaction history
- **Call Analytics**: Call recordings, transcripts, and AI-generated summaries
- **Multi-tenant**: Support for multiple businesses on a single platform
- **Real-time Dashboard**: Live call status, appointments, and metrics

### AI Agent Capabilities
- Intent detection (booking, rescheduling, cancelling, inquiries)
- Conversation context management
- Calendar availability checking
- Appointment confirmation with summaries
- Sentiment analysis and call summaries
- Human escalation when needed
- Multilingual support framework

### Integrations
- **Telephony**: Twilio/Vapi for inbound/outbound calls
- **Calendar**: Google Calendar, Outlook Calendar sync
- **CRM**: HubSpot, Zoho, Salesforce integration
- **Communication**: Email (SMTP), SMS notifications
- **Webhooks**: Custom webhook support for external integrations
- **Storage**: AWS S3 for call recordings

### Admin Dashboard
- Live appointment calendar
- Customer management interface
- Call recording and transcript access
- AI-generated call summaries and insights
- Business settings configuration
- Staff management
- Analytics and reporting
- API key management
- Billing and subscription management

## 🛠 Tech Stack

### Frontend
- **Framework**: Next.js 15 + React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State Management**: Zustand
- **HTTP Client**: Axios
- **UI Components**: Radix UI

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Background Jobs**: Celery
- **Authentication**: JWT + OAuth
- **API Docs**: OpenAPI/Swagger

### AI & Voice
- **AI Model**: OpenAI GPT-4 Turbo
- **Text-to-Speech**: OpenAI Voice API / Deepgram
- **Speech-to-Text**: Built into telephony provider
- **Conversation State**: Redis + In-memory management

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (reverse proxy + load balancing)
- **Deployment**: GitHub Actions CI/CD
- **Hosting**: DigitalOcean / AWS / Azure

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7+
- Git

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository>
cd ai-voice-receptionist
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` with your settings:

```env
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/business_assistant

# API Keys
OPENAI_API_KEY=sk-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...

# Optional: CRM/Calendar integrations
GOOGLE_CLIENT_ID=...
HUBSPOT_API_KEY=...
```

### 3. Start Services

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or manually:
# Start PostgreSQL, Redis, then run:
cd backend && pip install -r requirements.txt && python -m uvicorn app.main:app
cd frontend && npm install && npm run dev
```

### 4. Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Nginx (Production)**: http://localhost

## 📊 Project Structure

```
ai-voice-receptionist/
├── frontend/                 # Next.js dashboard application
│   ├── app/                 # Pages and layouts
│   ├── components/          # Reusable React components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities and API client
│   ├── styles/             # Global CSS and Tailwind
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API route handlers
│   │   ├── ai/             # AI conversation logic
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic validation schemas
│   │   ├── services/       # Business logic layer
│   │   ├── middleware/     # Custom middleware
│   │   ├── utils/          # Helper functions
│   │   ├── database/       # Database configuration
│   │   └── main.py         # FastAPI application entry
│   ├── requirements.txt     # Python dependencies
│   └── config.py            # Configuration settings
│
├── docker/                  # Docker configuration
│   ├── Dockerfile.backend   # Backend container
│   └── Dockerfile.frontend  # Frontend container
│
├── nginx/                   # Nginx configuration
│   └── nginx.conf          # Reverse proxy setup
│
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│
├── docker-compose.yml      # Multi-container orchestration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔐 Authentication

The system uses JWT tokens for API authentication:

1. **Register**: POST `/api/v1/auth/register`
2. **Login**: POST `/api/v1/auth/login`
3. **Get Token**: Login response includes `access_token`
4. **Use Token**: Include in headers: `Authorization: Bearer {token}`

## 📱 API Endpoints

### Authentication
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh-token
GET    /api/v1/auth/me
```

### Appointments
```
GET    /api/v1/appointments?business_id={id}
POST   /api/v1/appointments?business_id={id}
GET    /api/v1/appointments/{id}
PUT    /api/v1/appointments/{id}
DELETE /api/v1/appointments/{id}
GET    /api/v1/appointments/{staff_id}/availability
```

### Customers
```
GET    /api/v1/customers?business_id={id}
POST   /api/v1/customers?business_id={id}
GET    /api/v1/customers/{id}
PUT    /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
```

### Calls
```
GET    /api/v1/calls?business_id={id}
POST   /api/v1/calls?business_id={id}
GET    /api/v1/calls/{id}
PUT    /api/v1/calls/{id}
GET    /api/v1/calls/{id}/transcript
GET    /api/v1/calls/{id}/recording
```

### Analytics
```
GET    /api/v1/analytics/business/{business_id}
GET    /api/v1/analytics/calls/{business_id}
GET    /api/v1/analytics/appointments/{business_id}
```

### Business
```
GET    /api/v1/businesses/{id}
PUT    /api/v1/businesses/{id}
GET    /api/v1/businesses/{id}/settings
PUT    /api/v1/businesses/{id}/settings
```

## 🌐 Webhooks

### Incoming Call
```
POST /api/v1/webhooks/twilio/incoming-call
```

### Call Status Update
```
POST /api/v1/webhooks/twilio/call-status
```

### Recording Completed
```
POST /api/v1/webhooks/twilio/recording
```

## 🤖 AI Agent Configuration

The AI receptionist system is configured using a comprehensive system prompt. Customize behavior in:

**Backend**: `backend/app/ai/conversation.py`

Key configurations:
- AI voice (alloy, echo, fable, onyx, nova, shimmer)
- Temperature (0.0-1.0) for response creativity
- System prompt for behavioral guidance
- Intent detection keywords
- Conversation state machine

## 🗄 Database

### Migrations

Run database migrations:

```bash
# Generate migration (after changing models)
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Seed Data

```bash
cd backend
python -m app.database.seed
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Run services
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

### Production Considerations

1. **Environment Variables**: Set all secrets in `.env`
2. **SSL Certificate**: Configure in `nginx/ssl/`
3. **Database Backup**: Setup automated backups
4. **Monitoring**: Integrate with logging/monitoring service
5. **Rate Limiting**: Configured in nginx and FastAPI
6. **CORS**: Configure allowed origins in `backend/config.py`

### GitHub Actions CI/CD

Automated workflows for:
- Lint and format checks
- Unit and integration tests
- Docker image building and pushing
- Automatic deployment to staging/production

View workflows in `.github/workflows/`

## 📈 Monitoring

### Health Checks

```bash
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs
tail -f logs/app.log
```

### Metrics

Access metrics via:
- FastAPI docs: http://localhost:8000/docs
- Analytics endpoint: `/api/v1/analytics/business/{id}`

## 🔧 Configuration

### Backend Configuration

Edit `backend/config.py` to customize:
- Database connection
- Redis settings
- JWT parameters
- API settings
- OpenAI configuration
- Third-party integrations

### Frontend Configuration

Environment variables in `frontend/.env`:
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_APP_NAME`: Application name

## 📞 Twilio Integration

### Setup

1. Create Twilio account and get credentials
2. Set in `.env`:
   ```
   TWILIO_ACCOUNT_SID=ACxxxx...
   TWILIO_AUTH_TOKEN=xxxx...
   TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
   ```

3. Configure webhooks in Twilio dashboard:
   - Incoming call: `https://yourdomain.com/api/v1/webhooks/twilio/incoming-call`
   - Call status: `https://yourdomain.com/api/v1/webhooks/twilio/call-status`
   - Recording: `https://yourdomain.com/api/v1/webhooks/twilio/recording`

## 🔌 OpenAI Integration

1. Create OpenAI API key: https://platform.openai.com/api-keys
2. Set in `.env`:
   ```
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4-turbo
   OPENAI_VOICE_MODEL=tts-1-hd
   ```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **Backend Guide**: `docs/BACKEND.md`
- **Frontend Guide**: `docs/FRONTEND.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`
- **Architecture**: `docs/ARCHITECTURE.md`

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push branch: `git push origin feature/feature-name`
4. Create Pull Request

## 📄 License

Proprietary - All rights reserved

## 🆘 Support

For issues and questions:
- GitHub Issues: Create an issue on the repository
- Documentation: Check `docs/` folder
- Email: support@businessassistant.com

## 🎉 Acknowledgments

Built with modern technologies and best practices for production-ready applications.

---

**Last Updated**: December 2024
**Version**: 1.0.0
