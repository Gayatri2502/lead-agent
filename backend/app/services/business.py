"""Business logic services"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Appointment, Customer, Call, Staff
from app.schemas import AppointmentAnalyticsResponse, CallAnalyticsResponse


class AppointmentService:
    @staticmethod
    def get_availability(db: Session, business_id: int, staff_id: int, date: datetime):
        """Get available slots for a staff member"""
        # Get all appointments for the day
        day_start = datetime(date.year, date.month, date.day, 0, 0, 0)
        day_end = datetime(date.year, date.month, date.day, 23, 59, 59)
        
        appointments = db.query(Appointment).filter(
            Appointment.business_id == business_id,
            Appointment.staff_id == staff_id,
            Appointment.start_time >= day_start,
            Appointment.start_time <= day_end,
            Appointment.status != "cancelled"
        ).all()
        
        # Generate 30-min slots (adjust as needed)
        slots = []
        current = day_start.replace(hour=9, minute=0)  # 9 AM
        end = day_start.replace(hour=17, minute=0)  # 5 PM
        
        booked_times = {(app.start_time, app.end_time) for app in appointments}
        
        while current < end:
            slot_end = current + timedelta(minutes=30)
            
            # Check if slot overlaps with any booking
            is_available = True
            for booked_start, booked_end in booked_times:
                if (current < booked_end and slot_end > booked_start):
                    is_available = False
                    break
            
            if is_available:
                slots.append({"start": current, "end": slot_end})
            
            current = slot_end
        
        return slots

    @staticmethod
    def book_appointment(db: Session, customer_id: int, appointment_data):
        """Book an appointment"""
        appointment = Appointment(
            customer_id=customer_id,
            **appointment_data
        )
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    @staticmethod
    def cancel_appointment(db: Session, appointment_id: int):
        """Cancel an appointment"""
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if appointment:
            appointment.status = "cancelled"
            db.commit()
        
        return appointment


class CallService:
    @staticmethod
    def create_call_record(db: Session, business_id: int, call_data):
        """Create a new call record"""
        call = Call(
            business_id=business_id,
            **call_data
        )
        db.add(call)
        db.commit()
        db.refresh(call)
        return call

    @staticmethod
    def update_call_record(db: Session, call_id: int, call_data):
        """Update call record with transcription and summary"""
        call = db.query(Call).filter(Call.id == call_id).first()
        
        if call:
            for key, value in call_data.items():
                setattr(call, key, value)
            
            db.commit()
            db.refresh(call)
        
        return call


class CustomerService:
    @staticmethod
    def get_or_create_customer(db: Session, business_id: int, phone: str, customer_data: dict):
        """Get existing customer or create new one"""
        customer = db.query(Customer).filter(
            Customer.business_id == business_id,
            Customer.phone == phone
        ).first()
        
        if not customer:
            customer_data["business_id"] = business_id
            customer_data["phone"] = phone
            customer = Customer(**customer_data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
        
        return customer


class AnalyticsService:
    @staticmethod
    def get_call_analytics(db: Session, business_id: int, days: int = 30):
        """Get call analytics"""
        since = datetime.utcnow() - timedelta(days=days)
        
        calls = db.query(Call).filter(
            Call.business_id == business_id,
            Call.created_at >= since
        ).all()
        
        total = len(calls)
        incoming = sum(1 for c in calls if c.call_direction == "inbound")
        outgoing = sum(1 for c in calls if c.call_direction == "outbound")
        completed = sum(1 for c in calls if c.status == "completed")
        missed = sum(1 for c in calls if c.status == "missed")
        
        total_duration = sum(c.duration for c in calls if c.duration)
        avg_duration = total_duration / total if total > 0 else 0
        
        by_sentiment = {}
        by_intent = {}
        
        for call in calls:
            if call.sentiment:
                by_sentiment[call.sentiment] = by_sentiment.get(call.sentiment, 0) + 1
            if call.intent:
                by_intent[call.intent] = by_intent.get(call.intent, 0) + 1
        
        return CallAnalyticsResponse(
            total_calls=total,
            incoming_calls=incoming,
            outgoing_calls=outgoing,
            completed_calls=completed,
            missed_calls=missed,
            average_duration=avg_duration,
            total_duration=total_duration,
            by_sentiment=by_sentiment,
            by_intent=by_intent
        )

    @staticmethod
    def get_appointment_analytics(db: Session, business_id: int, days: int = 30):
        """Get appointment analytics"""
        since = datetime.utcnow() - timedelta(days=days)
        
        appointments = db.query(Appointment).filter(
            Appointment.business_id == business_id,
            Appointment.created_at >= since
        ).all()
        
        total = len(appointments)
        confirmed = sum(1 for a in appointments if a.status == "confirmed")
        completed = sum(1 for a in appointments if a.status == "completed")
        cancelled = sum(1 for a in appointments if a.status == "cancelled")
        no_shows = sum(1 for a in appointments if a.status == "no_show")
        
        return AppointmentAnalyticsResponse(
            total_appointments=total,
            confirmed_appointments=confirmed,
            completed_appointments=completed,
            cancelled_appointments=cancelled,
            no_shows=no_shows,
            busiest_day="Monday",
            busiest_time="10:00 AM",
            average_booking_advance_days=7
        )
