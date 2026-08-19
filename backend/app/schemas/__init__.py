"""Pydantic schemas for API requests and responses"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any


# ==================== Business Schemas ====================
class BusinessCreate(BaseModel):
    name: str
    business_type: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    timezone: str = "UTC"
    appointment_duration: int = 30
    booking_advance_days: int = 90
    cancellation_notice_hours: int = 24


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    business_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    timezone: Optional[str] = None
    appointment_duration: Optional[int] = None
    booking_advance_days: Optional[int] = None
    cancellation_notice_hours: Optional[int] = None


class BusinessResponse(BaseModel):
    id: int
    name: str
    business_type: str
    address: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    timezone: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== User/Auth Schemas ====================
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    role: str = "receptionist"

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ==================== Customer Schemas ====================
class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    language: str = "en"
    medical_history: Optional[str] = None


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    language: Optional[str] = None
    medical_history: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: Optional[str]
    address: Optional[str]
    is_returning: bool
    language: str
    created_at: datetime
    last_appointment: Optional[datetime]

    class Config:
        from_attributes = True


# ==================== Staff Schemas ====================
class StaffCreate(BaseModel):
    name: str
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    available_days: Optional[List[int]] = None  # 1-7 (Mon-Sun)
    available_hours: Optional[Dict[str, str]] = None


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    available_days: Optional[List[int]] = None
    available_hours: Optional[Dict[str, str]] = None


class StaffResponse(BaseModel):
    id: int
    name: str
    specialization: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Service Schemas ====================
class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    duration: int = 30
    price: Optional[float] = None


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    duration: int
    price: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True


# ==================== Appointment Schemas ====================
class AppointmentCreate(BaseModel):
    customer_id: int
    staff_id: Optional[int] = None
    service_id: Optional[int] = None
    start_time: datetime
    duration: Optional[int] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    special_requests: Optional[str] = None
    booking_source: str = "phone"


class AppointmentUpdate(BaseModel):
    staff_id: Optional[int] = None
    service_id: Optional[int] = None
    start_time: Optional[datetime] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    customer_id: int
    staff_id: Optional[int]
    service_id: Optional[int]
    start_time: datetime
    end_time: datetime
    duration: int
    status: str
    reason: Optional[str]
    notes: Optional[str]
    booking_source: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Call Schemas ====================
class CallCreate(BaseModel):
    customer_id: Optional[int] = None
    phone_number: str
    call_direction: str = "inbound"
    transcript: Optional[str] = None
    recording_url: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    intent: Optional[str] = None


class CallResponse(BaseModel):
    id: int
    customer_id: Optional[int]
    call_id: str
    phone_number: str
    call_direction: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: int
    transcript: Optional[str]
    summary: Optional[str]
    sentiment: Optional[str]
    intent: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== API Key Schemas ====================
class APIKeyCreate(BaseModel):
    name: str
    scopes: Optional[List[str]] = None


class APIKeyResponse(BaseModel):
    id: int
    name: str
    key: str
    is_active: bool
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Business Settings Schemas ====================
class BusinessSettingsUpdate(BaseModel):
    ai_voice: Optional[str] = None
    ai_temperature: Optional[float] = None
    enable_sms_reminders: Optional[bool] = None
    enable_email_reminders: Optional[bool] = None
    reminder_before_hours: Optional[int] = None
    sync_google_calendar: Optional[bool] = None
    sync_outlook_calendar: Optional[bool] = None
    crm_type: Optional[str] = None
    crm_integration_enabled: Optional[bool] = None


class BusinessSettingsResponse(BaseModel):
    id: int
    business_id: int
    ai_voice: str
    ai_temperature: float
    enable_sms_reminders: bool
    enable_email_reminders: bool
    reminder_before_hours: int
    sync_google_calendar: bool
    sync_outlook_calendar: bool
    crm_type: Optional[str]
    crm_integration_enabled: bool

    class Config:
        from_attributes = True


# ==================== Analytics Schemas ====================
class CallAnalyticsResponse(BaseModel):
    total_calls: int
    incoming_calls: int
    outgoing_calls: int
    completed_calls: int
    missed_calls: int
    average_duration: float
    total_duration: int
    by_sentiment: Dict[str, int]
    by_intent: Dict[str, int]


class AppointmentAnalyticsResponse(BaseModel):
    total_appointments: int
    confirmed_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    no_shows: int
    busiest_day: str
    busiest_time: str
    average_booking_advance_days: float


class BusinessAnalyticsResponse(BaseModel):
    calls: CallAnalyticsResponse
    appointments: AppointmentAnalyticsResponse
    customers: Dict[str, int]
    revenue: Optional[float]
