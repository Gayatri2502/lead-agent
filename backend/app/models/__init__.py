"""SQLAlchemy models for the application"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, Float, ForeignKey, Enum, Index, JSON
from sqlalchemy.orm import relationship
from app.database.db import Base
import enum


class Business(Base):
    """Business/Organization model"""
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    business_type = Column(String(100), nullable=False)  # Doctor, Dentist, Salon, etc.
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)
    timezone = Column(String(50), default="UTC")
    logo_url = Column(String(500), nullable=True)
    
    # Business hours (stored as JSON)
    working_hours = Column(JSON, nullable=True)  # {mon: {open: "09:00", close: "17:00"}, ...}
    holiday_schedule = Column(JSON, nullable=True)  # {date: "reason"}
    
    # Configuration
    appointment_duration = Column(Integer, default=30)  # in minutes
    booking_advance_days = Column(Integer, default=90)
    cancellation_notice_hours = Column(Integer, default=24)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="business", cascade="all, delete-orphan")
    staff = relationship("Staff", back_populates="business", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="business", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="business", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="business", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="business", cascade="all, delete-orphan")
    settings = relationship("BusinessSettings", back_populates="business", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="business", cascade="all, delete-orphan")
    
    __table_args__ = (Index("idx_business_name", "name"),)


class User(Base):
    """User/Staff member model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="receptionist")  # admin, manager, receptionist
    
    # Profile
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Metadata
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="users")
    
    __table_args__ = (Index("idx_user_email", "email"), Index("idx_user_business_id", "business_id"))


class Staff(Base):
    """Staff/Healthcare provider model"""
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    name = Column(String(255), nullable=False)
    specialization = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    photo_url = Column(String(500), nullable=True)
    
    # Availability
    available_days = Column(JSON, nullable=True)  # [1,2,3,4,5] for Mon-Fri
    available_hours = Column(JSON, nullable=True)  # {start: "09:00", end: "17:00"}
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="staff")
    appointments = relationship("Appointment", back_populates="staff")
    
    __table_args__ = (Index("idx_staff_business_id", "business_id"),)


class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    address = Column(String(500), nullable=True)
    
    # Customer info
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    language = Column(String(10), default="en")
    
    # Medical/Service history
    medical_history = Column(Text, nullable=True)
    preferences = Column(JSON, nullable=True)
    
    # Status
    is_returning = Column(Boolean, default=False)
    do_not_call = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_appointment = Column(DateTime, nullable=True)
    
    # Relationships
    business = relationship("Business", back_populates="customers")
    appointments = relationship("Appointment", back_populates="customer", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="customer", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_customer_phone", "phone"),
        Index("idx_customer_email", "email"),
        Index("idx_customer_business_id", "business_id"),
    )


class Service(Base):
    """Service/Treatment offered by business"""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Integer, default=30)  # in minutes
    price = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = relationship("Business", back_populates="services")
    appointments = relationship("Appointment", back_populates="service")
    
    __table_args__ = (Index("idx_service_business_id", "business_id"),)


class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class Appointment(Base):
    """Appointment model"""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    
    # Appointment details
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    duration = Column(Integer, default=30)  # in minutes
    
    # Status
    status = Column(String(50), default=AppointmentStatus.PENDING, index=True)
    
    # Reason and notes
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    special_requests = Column(Text, nullable=True)
    
    # Booking source
    booking_source = Column(String(50), default="phone")  # phone, web, email, etc.
    
    # Reminders
    reminder_sent = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    call_id = Column(Integer, ForeignKey("calls.id"), nullable=True)
    
    # Relationships
    business = relationship("Business", back_populates="appointments")
    customer = relationship("Customer", back_populates="appointments")
    staff = relationship("Staff", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    call = relationship("Call", back_populates="appointment")
    
    __table_args__ = (
        Index("idx_appointment_start_time", "start_time"),
        Index("idx_appointment_customer_id", "customer_id"),
        Index("idx_appointment_staff_id", "staff_id"),
        Index("idx_appointment_business_id", "business_id"),
    )


class Call(Base):
    """Phone call/conversation record"""
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    
    # Call details
    call_id = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=False)
    call_direction = Column(String(20), default="inbound")  # inbound, outbound
    
    # Duration
    start_time = Column(DateTime, default=datetime.utcnow, index=True)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, default=0)  # in seconds
    
    # Recording
    recording_url = Column(String(500), nullable=True)
    recording_duration = Column(Integer, nullable=True)
    
    # Transcription
    transcript = Column(Text, nullable=True)
    transcript_language = Column(String(10), default="en")
    
    # AI Analysis
    summary = Column(Text, nullable=True)
    sentiment = Column(String(50), nullable=True)  # positive, neutral, negative
    intent = Column(String(100), nullable=True)  # book, reschedule, cancel, inquire, etc.
    
    # Status
    status = Column(String(50), default="completed")  # completed, missed, failed, etc.
    escalated_to_human = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="calls")
    customer = relationship("Customer", back_populates="calls")
    appointment = relationship("Appointment", back_populates="call")
    
    __table_args__ = (
        Index("idx_call_start_time", "start_time"),
        Index("idx_call_customer_id", "customer_id"),
        Index("idx_call_business_id", "business_id"),
    )


class BusinessSettings(Base):
    """Business configuration and settings"""
    __tablename__ = "business_settings"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, unique=True)
    
    # AI Configuration
    ai_voice = Column(String(50), default="alloy")  # Voice model
    ai_temperature = Column(Float, default=0.7)
    ai_system_prompt = Column(Text, nullable=True)
    
    # Notification settings
    enable_sms_reminders = Column(Boolean, default=True)
    enable_email_reminders = Column(Boolean, default=True)
    reminder_before_hours = Column(Integer, default=24)
    
    # Calendar sync
    sync_google_calendar = Column(Boolean, default=False)
    sync_outlook_calendar = Column(Boolean, default=False)
    
    # CRM Integration
    crm_type = Column(String(50), nullable=True)  # hubspot, zoho, salesforce
    crm_integration_enabled = Column(Boolean, default=False)
    
    # Feature flags
    enable_video_calls = Column(Boolean, default=False)
    enable_custom_branding = Column(Boolean, default=False)
    enable_advanced_analytics = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = relationship("Business", back_populates="settings")


class APIKey(Base):
    """API keys for business integrations"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    key = Column(String(255), unique=True, nullable=False, index=True)
    secret = Column(String(255), nullable=False)
    
    # Permissions
    scopes = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    business = relationship("Business", back_populates="api_keys")
    
    __table_args__ = (Index("idx_apikey_business_id", "business_id"),)


class AuditLog(Base):
    """Audit logging for compliance"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    action = Column(String(255), nullable=False)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer, nullable=True)
    
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index("idx_auditlog_business_id", "business_id"),
        Index("idx_auditlog_created_at", "created_at"),
    )
