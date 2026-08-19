"""
ARCHITECTURE DOCUMENTATION

System design and component overview.
"""

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    End User / Customer                        │
└────────┬────────────────────────────────────────────────────┘
         │
         │ Phone Call (PSTN)
         ↓
┌─────────────────────────────────────────────────────────────┐
│            Twilio/Vapi (Telephony Provider)                 │
│        - Receives incoming calls                             │
│        - Routes to AI agent                                  │
│        - Records conversations                              │
└────────┬────────────────────────────────────────────────────┘
         │
         │ WebSocket / HTTP
         ↓
┌─────────────────────────────────────────────────────────────┐
│                  Nginx (Reverse Proxy)                       │
│        - Load balancing                                      │
│        - SSL/TLS termination                                │
│        - Rate limiting                                       │
└────┬──────────────────────────────────────┬─────────────────┘
     │                                      │
     │ WebSocket                            │ HTTP/REST
     ↓                                      ↓
┌──────────────────┐         ┌───────────────────────┐
│  Next.js         │         │   FastAPI Backend     │
│  Frontend        │         │                       │
│                  │         │ - API Handlers        │
│ - Dashboard      │         │ - AI Logic            │
│ - Real-time UI   │         │ - DB Queries          │
│ - Call Player    │         │ - Integrations        │
│ - Charts         │         │ - Authentication      │
└────────┬─────────┘         └────────┬──────────────┘
         │                           │
         │                           │ SQL
         │                    ┌──────┴──────┐
         │                    ↓             ↓
         │              ┌──────────────────────────┐
         │              │   PostgreSQL Database    │
         │              │                          │
         │              │ - Businesses             │
         │              │ - Users                  │
         │              │ - Appointments           │
         │              │ - Customers              │
         │              │ - Calls                  │
         │              │ - Analytics              │
         │              └──────────────────────────┘
         │
         │ Cache / Session
         ↓
      ┌──────────────┐
      │    Redis     │
      │ - Sessions   │
      │ - Cache      │
      │ - Queues     │
      └──────────────┘

External Integrations:
- OpenAI: AI/Voice API
- Twilio: Telephony
- Google Calendar: Calendar sync
- AWS S3: Recording storage
- SMTP: Email service
- SMS: Message service
- HubSpot/Zoho/Salesforce: CRM
```

## Component Details

### Frontend (Next.js + React)

**Responsibilities**:
- User interface for dashboard
- Real-time appointment management
- Call history viewing
- Analytics visualization
- Business settings management

**Key Libraries**:
- Next.js: Framework
- Tailwind CSS: Styling
- Zustand: State management
- Axios: HTTP client
- Chart.js: Charting

### Backend (FastAPI)

**Architecture Layers**:
1. **API Layer** (`app/api/`): Route handlers, request/response
2. **Service Layer** (`app/services/`): Business logic
3. **AI Layer** (`app/ai/`): Conversation, intent, summarization
4. **Model Layer** (`app/models/`): SQLAlchemy ORM definitions
5. **Schema Layer** (`app/schemas/`): Pydantic validation
6. **Database Layer** (`app/database/`): Connection, migrations
7. **Middleware** (`app/middleware/`): Logging, auth, rate limiting
8. **Utils** (`app/utils/`): Helpers, security, validation

**Key Features**:
- JWT authentication with role-based access
- Request validation with Pydantic
- Comprehensive logging with structlog
- Error handling and status codes
- Rate limiting middleware
- CORS configuration

### Database (PostgreSQL)

**Schema**:
- **Businesses**: Multi-tenant separation
- **Users**: Team members with roles
- **Staff**: Healthcare providers/service staff
- **Customers**: Client profiles
- **Appointments**: Scheduled bookings
- **Calls**: Phone call records with transcripts
- **Services**: Available services/treatments
- **Settings**: Business configuration
- **APIKeys**: Third-party integrations
- **AuditLogs**: Compliance tracking

**Indexes**: Optimized for common queries
**Foreign Keys**: Referential integrity
**Migrations**: Alembic version control

### Cache Layer (Redis)

**Purpose**:
- Session storage
- Conversation state management
- Rate limiting counters
- Job queue (Celery)
- Temporary cache data

### Integrations

**Twilio**:
- Webhook receiving incoming calls
- Audio streaming to AI
- Voice response playback
- Recording storage

**OpenAI**:
- GPT-4 for conversation logic
- Text-to-speech for voice response
- Sentiment analysis and summarization

**Calendar Providers**:
- Google Calendar API: Availability checking
- Outlook API: Schedule sync

**CRM Systems**:
- HubSpot API: Contact sync
- Zoho CRM: Lead tracking
- Salesforce: Enterprise integration

**Storage**:
- AWS S3: Call recordings and transcripts

## Data Flow

### Incoming Call Flow

1. **Call Received**
   - Twilio webhook receives incoming call
   - Extracts phone number, call SID

2. **Create Call Record**
   - Backend creates Call record in database
   - Initializes ConversationContext in Redis

3. **AI Processing**
   - Audio streamed to OpenAI
   - GPT-4 processes conversation
   - Intent detected (book, cancel, reschedule, etc.)

4. **Action Execution**
   - If booking: Check availability, create Appointment
   - If reschedule: Update existing Appointment
   - If cancel: Mark Appointment as cancelled
   - If inquiry: Provide information

5. **Call Completion**
   - Transcription generated
   - Summary created with AI
   - Sentiment analyzed
   - Customer matched/created
   - Call record updated with all metadata
   - Recording uploaded to S3

### Dashboard Real-time Updates

1. User views dashboard
2. Frontend fetches data via REST API
3. Real-time WebSocket connection for live updates
4. Charts and counters update automatically
5. Click to view detailed records

## Security Architecture

**Authentication**: JWT tokens with expiration
**Authorization**: Role-based access control (RBAC)
**Encryption**: HTTPS with SSL/TLS
**Input Validation**: Pydantic schemas enforce types
**Rate Limiting**: Per-IP request throttling
**CORS**: Configured allowed origins
**Logging**: Audit trails for compliance
**Secrets**: Environment variables, not in code

## Scalability Considerations

**Horizontal Scaling**:
- Stateless API servers behind load balancer
- Database read replicas
- Distributed Redis cluster
- CDN for static assets

**Vertical Scaling**:
- Increase container resources
- Upgrade database machine
- Increase Redis memory

**Performance Optimization**:
- Database query optimization with indexes
- Caching with Redis
- API response compression
- Frontend code splitting
- Image optimization
- Rate limiting prevents overload

## Deployment Strategy

**Development**: Local docker-compose
**Staging**: Full production setup for testing
**Production**: Multi-container orchestration

**CI/CD Pipeline**:
- GitHub Actions: Lint, test, build
- Docker builds: Backend + Frontend
- Registry: Docker Hub / ECR
- Deployment: docker-compose or Kubernetes

## Monitoring & Observability

**Logs**:
- Structured logging with JSON
- Centralized log aggregation
- Error tracking and alerting

**Metrics**:
- API response times
- Error rates
- Database query performance
- Cache hit rates
- Call success rates

**Alerting**:
- Critical errors
- Resource exhaustion
- High latency
- Service downtime

## Future Enhancements

- Kubernetes orchestration
- Machine learning for better NLP
- Advanced analytics and BI
- Video call support
- Multi-language AI models
- Blockchain for compliance
- Advanced security (2FA, etc.)
