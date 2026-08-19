"""
Backend Documentation

FastAPI backend API documentation and development guide.
"""

## Backend Overview

### Technology Stack
- **Framework**: FastAPI (modern, fast, production-ready)
- **Server**: Uvicorn (ASGI server)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for sessions and caching
- **Task Queue**: Celery for background jobs
- **Auth**: JWT tokens with role-based access
- **Logging**: Structlog with JSON formatting

### Architecture Layers

1. **API Layer** (`app/api/`): Route handlers
2. **Service Layer** (`app/services/`): Business logic
3. **Model Layer** (`app/models/`): Database models
4. **Schema Layer** (`app/schemas/`): Data validation
5. **Middleware**: Authentication, logging, rate limiting

## Running the Backend

### Development

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

API runs at: `http://localhost:8000`
Docs at: `http://localhost:8000/docs`

### Production

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

Or with Docker:
```bash
docker build -f docker/Dockerfile.backend -t backend:latest .
docker run -p 8000:8000 backend:latest
```

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── appointments.py  # Appointment CRUD
│   │   ├── customers.py     # Customer CRUD
│   │   ├── calls.py         # Call records
│   │   ├── analytics.py     # Analytics endpoints
│   │   ├── webhooks.py      # Twilio/integration webhooks
│   │   └── business.py      # Business settings
│   │
│   ├── ai/
│   │   └── conversation.py  # AI agent logic
│   │
│   ├── models/
│   │   └── __init__.py      # SQLAlchemy ORM models
│   │
│   ├── schemas/
│   │   └── __init__.py      # Pydantic validation schemas
│   │
│   ├── services/
│   │   └── business.py      # Business logic
│   │
│   ├── middleware/
│   │   └── __init__.py      # Custom middleware
│   │
│   ├── utils/
│   │   ├── security.py      # JWT, password hashing
│   │   └── helpers.py       # Utility functions
│   │
│   ├── database/
│   │   └── db.py            # Database configuration
│   │
│   └── main.py              # FastAPI application
│
├── tests/                   # Test suite
│   ├── test_api.py
│   └── test_ai.py
│
├── requirements.txt         # Python dependencies
├── config.py                # Configuration settings
└── alembic.ini              # Database migrations
```

## Database Models

### Key Models

**Business**
```python
id: int (PK)
name: str
business_type: str
address: str
timezone: str
working_hours: JSON
```

**User**
```python
id: int (PK)
business_id: int (FK)
email: str
role: str (admin, manager, receptionist)
```

**Appointment**
```python
id: int (PK)
business_id: int (FK)
customer_id: int (FK)
staff_id: int (FK)
start_time: datetime
status: str (pending, confirmed, completed, cancelled)
```

**Call**
```python
id: int (PK)
business_id: int (FK)
customer_id: int (FK)
call_id: str (unique)
transcript: str
summary: str
sentiment: str
intent: str
recording_url: str
```

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Endpoints

### Authentication

```
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh-token
GET  /api/v1/auth/me
```

### Business

```
GET    /api/v1/businesses/{id}
PUT    /api/v1/businesses/{id}
GET    /api/v1/businesses/{id}/settings
PUT    /api/v1/businesses/{id}/settings
GET    /api/v1/health
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
GET /api/v1/analytics/business/{business_id}
GET /api/v1/analytics/calls/{business_id}
GET /api/v1/analytics/appointments/{business_id}
```

### Webhooks

```
POST /api/v1/webhooks/twilio/incoming-call
POST /api/v1/webhooks/twilio/call-status
POST /api/v1/webhooks/twilio/recording
```

## Authentication

### Login Flow

1. **Register**: POST `/auth/register`
   - Email, password, name
   - Creates user and business

2. **Login**: POST `/auth/login`
   - Email and password
   - Returns JWT token

3. **Use Token**: Add to headers
   ```
   Authorization: Bearer {token}
   ```

4. **Refresh**: POST `/auth/refresh-token`
   - Extends session

### Roles

- **Admin**: Full access
- **Manager**: Manage staff and appointments
- **Receptionist**: Handle calls and bookings

## Configuration

Edit `backend/config.py`:

```python
# Database
DATABASE_URL = "postgresql://user:password@localhost/db"

# API
API_PORT = 8000
API_DEBUG = False

# JWT
SECRET_KEY = "your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OpenAI
OPENAI_API_KEY = "sk-..."

# Twilio
TWILIO_ACCOUNT_SID = "AC..."
TWILIO_AUTH_TOKEN = "..."
```

## Middleware

### Request Logging

All requests logged with:
- Method, path, status code
- Client IP, user agent
- Duration and response time

### Rate Limiting

- 100 requests/minute for API
- 50 requests/minute for general
- Per-IP tracking

### Authentication

- JWT validation on protected routes
- Token expiration checking
- Role-based access control

## Adding New Endpoints

### 1. Create Schema

```python
# app/schemas/__init__.py
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
    id: int
    name: str
```

### 2. Create Route

```python
# app/api/items.py
from fastapi import APIRouter, Depends
from app.database.db import get_db

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[ItemResponse])
def list_items(business_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.business_id == business_id).all()

@router.post("/", response_model=ItemResponse)
def create_item(business_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(business_id=business_id, **item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

### 3. Include Router

```python
# app/main.py
from app.api import items
app.include_router(items.router, prefix=settings.api_prefix)
```

## Testing

### Run Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=app
```

### Write Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

## Error Handling

### Standard Errors

```python
from fastapi import HTTPException

# Not found
raise HTTPException(status_code=404, detail="Item not found")

# Unauthorized
raise HTTPException(status_code=401, detail="Not authenticated")

# Conflict
raise HTTPException(status_code=409, detail="Item already exists")
```

### Validation Errors

Pydantic automatically validates:
```python
class ItemCreate(BaseModel):
    name: str  # Required
    age: int = 25  # Optional with default
    email: EmailStr  # Email validation
```

## Performance Tips

1. **Database Indexing**: Add indexes to frequently queried columns
2. **Eager Loading**: Load related data efficiently with joins
3. **Caching**: Use Redis for frequently accessed data
4. **Async**: Use async functions for I/O operations
5. **Pagination**: Limit query results

## Logging

### Access Logs

Automatically logged via middleware:
- Request details
- Response status
- Processing time

### Application Logs

```python
import logging
logger = logging.getLogger(__name__)

logger.info("User logged in", extra={"user_id": user.id})
logger.error("Database error", exc_info=True)
```

## Debugging

### Enable Debug Mode

```python
# config.py
DEBUG = True
```

### Interactive Debugging

```bash
# Use pdb
python -m pdb -m uvicorn app.main:app

# Or use debugger in code
import pdb; pdb.set_trace()
```

### Inspect Database

```bash
# Connect to database
psql postgresql://user:password@localhost/db

# Query data
SELECT * FROM appointments;
```

## Deployment Checklist

- [ ] Set all environment variables
- [ ] Run database migrations
- [ ] Configure CORS origins
- [ ] Set SECRET_KEY to strong value
- [ ] Disable debug mode
- [ ] Configure SSL/TLS
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test all integrations
- [ ] Load test the API

## Troubleshooting

**Database connection error**
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check network connectivity

**Import errors**
- Verify all files are in correct directories
- Check __init__.py files exist
- Reinstall requirements: `pip install -r requirements.txt`

**Authentication issues**
- Verify JWT secret key is set
- Check token hasn't expired
- Verify Authorization header format

**Slow responses**
- Check database query performance
- Add indexes to frequently queried columns
- Enable query logging: `SQLALCHEMY_ECHO = True`
