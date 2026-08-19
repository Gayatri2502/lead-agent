"""Call endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db import get_db
from app.schemas import CallCreate, CallResponse
from app.models import Call, Business

router = APIRouter(prefix="/calls", tags=["calls"])


@router.get("/", response_model=list[CallResponse])
def list_calls(
    business_id: int,
    skip: int = Query(0),
    limit: int = Query(100),
    status: str = Query(None),
    db: Session = Depends(get_db)
):
    """List calls for a business"""
    query = db.query(Call).filter(Call.business_id == business_id)
    
    if status:
        query = query.filter(Call.status == status)
    
    calls = query.order_by(Call.start_time.desc()).offset(skip).limit(limit).all()
    return calls


@router.get("/{call_id}", response_model=CallResponse)
def get_call(call_id: int, db: Session = Depends(get_db)):
    """Get call details"""
    call = db.query(Call).filter(Call.id == call_id).first()
    
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    
    return call


@router.post("/", response_model=CallResponse)
def create_call(
    business_id: int,
    call_data: CallCreate,
    db: Session = Depends(get_db)
):
    """Create new call record"""
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    # Generate unique call ID
    from app.utils.helpers import generate_call_id
    unique_call_id = generate_call_id()
    
    # Create call record
    call = Call(
        business_id=business_id,
        call_id=unique_call_id,
        **call_data.dict()
    )
    
    db.add(call)
    db.commit()
    db.refresh(call)
    
    return call


@router.put("/{call_id}")
def update_call(
    call_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    """Update call with transcription, summary, sentiment"""
    call = db.query(Call).filter(Call.id == call_id).first()
    
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    
    # Update fields
    for field, value in update_data.items():
        if hasattr(call, field):
            setattr(call, field, value)
    
    # Set end time if duration is provided
    if "duration" in update_data and not call.end_time:
        from datetime import timedelta
        call.end_time = call.start_time + timedelta(seconds=update_data["duration"])
    
    db.commit()
    db.refresh(call)
    return call


@router.get("/{call_id}/transcript")
def get_transcript(call_id: int, db: Session = Depends(get_db)):
    """Get call transcript"""
    call = db.query(Call).filter(Call.id == call_id).first()
    
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    
    return {
        "call_id": call.id,
        "transcript": call.transcript,
        "summary": call.summary,
        "sentiment": call.sentiment,
        "intent": call.intent
    }


@router.get("/{call_id}/recording")
def get_recording(call_id: int, db: Session = Depends(get_db)):
    """Get call recording URL"""
    call = db.query(Call).filter(Call.id == call_id).first()
    
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    
    return {
        "call_id": call.id,
        "recording_url": call.recording_url,
        "duration": call.recording_duration
    }
