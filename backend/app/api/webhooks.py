"""Webhook endpoints for Twilio and integrations"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import json
import logging

from app.database.db import get_db
from app.models import Call, Business
from app.ai.conversation import CallSummarizer, SentimentAnalyzer
from app.services.business import CallService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger(__name__)


@router.post("/twilio/incoming-call")
async def handle_incoming_call(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle incoming Twilio call webhook"""
    try:
        body = await request.form()
        
        # Extract call details
        call_sid = body.get("CallSid")
        from_number = body.get("From")
        to_number = body.get("To")
        
        logger.info(f"Incoming call from {from_number} to {to_number}")
        
        # Find business by phone number (simplified)
        business = db.query(Business).filter(Business.phone == to_number).first()
        if not business:
            return {"error": "Business not found"}
        
        # Create call record
        call_data = {
            "phone_number": from_number,
            "call_direction": "inbound",
            "status": "in_progress"
        }
        
        call = CallService.create_call_record(db, business.id, call_data)
        
        # Return TwiML response (simplified)
        return {
            "message": f"Call {call_sid} received",
            "call_id": call.id,
            "business_id": business.id
        }
    
    except Exception as e:
        logger.error(f"Error handling incoming call: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/twilio/call-status")
async def handle_call_status(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Twilio call status update webhook"""
    try:
        body = await request.form()
        
        call_sid = body.get("CallSid")
        call_status = body.get("CallStatus")
        
        # Find call record
        call = db.query(Call).filter(Call.call_id == call_sid).first()
        if not call:
            return {"status": "call not found"}
        
        # Update call status
        call.status = call_status
        
        # If completed, generate summary
        if call_status == "completed":
            if call.transcript:
                call.summary = CallSummarizer.generate_summary(
                    call.transcript,
                    call.intent or "general"
                )
                call.sentiment = SentimentAnalyzer.analyze(call.transcript)
        
        db.commit()
        
        return {"message": "Status updated", "status": call_status}
    
    except Exception as e:
        logger.error(f"Error handling call status: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/twilio/recording")
async def handle_recording(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle recording completion webhook"""
    try:
        body = await request.form()
        
        call_sid = body.get("CallSid")
        recording_url = body.get("RecordingUrl")
        recording_sid = body.get("RecordingSid")
        
        call = db.query(Call).filter(Call.call_id == call_sid).first()
        if not call:
            return {"status": "call not found"}
        
        call.recording_url = recording_url
        db.commit()
        
        logger.info(f"Recording saved for call {call_sid}: {recording_url}")
        
        return {"message": "Recording saved"}
    
    except Exception as e:
        logger.error(f"Error handling recording: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/google-calendar/sync")
async def sync_google_calendar(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Sync Google Calendar with appointments"""
    # Implementation would go here
    return {"message": "Google Calendar sync initiated"}


@router.post("/outlook/sync")
async def sync_outlook_calendar(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Sync Outlook Calendar with appointments"""
    # Implementation would go here
    return {"message": "Outlook Calendar sync initiated"}
