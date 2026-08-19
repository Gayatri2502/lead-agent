"""Appointment endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.db import get_db
from app.schemas import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from app.models import Appointment, Business
from app.services.business import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/", response_model=list[AppointmentResponse])
def list_appointments(
    business_id: int,
    skip: int = Query(0),
    limit: int = Query(100),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """List appointments for a business"""
    query = db.query(Appointment).filter(Appointment.business_id == business_id)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Get appointment details"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    return appointment


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    business_id: int,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """Create new appointment"""
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    # Check availability
    if appointment_data.staff_id:
        existing = db.query(Appointment).filter(
            Appointment.staff_id == appointment_data.staff_id,
            Appointment.start_time <= appointment_data.start_time,
            Appointment.end_time > appointment_data.start_time,
            Appointment.status != "cancelled"
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Time slot not available"
            )
    
    # Create appointment
    duration = appointment_data.duration or business.appointment_duration
    end_time = appointment_data.start_time + timedelta(minutes=duration)
    
    appointment = Appointment(
        business_id=business_id,
        customer_id=appointment_data.customer_id,
        staff_id=appointment_data.staff_id,
        service_id=appointment_data.service_id,
        start_time=appointment_data.start_time,
        end_time=end_time,
        duration=duration,
        status="confirmed",
        reason=appointment_data.reason,
        notes=appointment_data.notes,
        special_requests=appointment_data.special_requests,
        booking_source=appointment_data.booking_source
    )
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """Update appointment"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    # Update fields
    for field, value in update_data.dict(exclude_unset=True).items():
        if field == "start_time" and value:
            appointment.start_time = value
            appointment.end_time = value + timedelta(minutes=appointment.duration)
        else:
            setattr(appointment, field, value)
    
    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """Cancel appointment"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    
    appointment.status = "cancelled"
    db.commit()
    
    return {"message": "Appointment cancelled"}


@router.get("/{staff_id}/availability")
def get_staff_availability(
    staff_id: int,
    date: str,
    db: Session = Depends(get_db)
):
    """Get available time slots for staff"""
    try:
        date_obj = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    
    slots = AppointmentService.get_availability(db, None, staff_id, date_obj)
    return {"slots": slots}
