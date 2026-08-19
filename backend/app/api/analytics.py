"""Analytics endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import BusinessAnalyticsResponse
from app.services.business import AnalyticsService
from app.models import Business

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/business/{business_id}")
def get_business_analytics(
    business_id: int,
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a business"""
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    # Get analytics
    calls_analytics = AnalyticsService.get_call_analytics(db, business_id, days)
    appointments_analytics = AnalyticsService.get_appointment_analytics(db, business_id, days)
    
    return {
        "calls": calls_analytics,
        "appointments": appointments_analytics,
        "customers": {
            "total": 0,
            "new": 0,
            "returning": 0
        },
        "revenue": 0
    }


@router.get("/calls/{business_id}")
def get_call_analytics(
    business_id: int,
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """Get call analytics"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    return AnalyticsService.get_call_analytics(db, business_id, days)


@router.get("/appointments/{business_id}")
def get_appointment_analytics(
    business_id: int,
    days: int = Query(30),
    db: Session = Depends(get_db)
):
    """Get appointment analytics"""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    return AnalyticsService.get_appointment_analytics(db, business_id, days)
