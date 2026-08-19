"""Business and settings endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import BusinessResponse, BusinessUpdate, BusinessCreate, BusinessSettingsResponse, BusinessSettingsUpdate
from app.models import Business, BusinessSettings

router = APIRouter(tags=["business"])


@router.get("/businesses/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    """Get business details"""
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    return business


@router.put("/businesses/{business_id}", response_model=BusinessResponse)
def update_business(
    business_id: int,
    update_data: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """Update business information"""
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    # Update fields
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(business, field, value)
    
    db.commit()
    db.refresh(business)
    return business


@router.get("/businesses/{business_id}/settings", response_model=BusinessSettingsResponse)
def get_business_settings(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get business settings"""
    settings = db.query(BusinessSettings).filter(
        BusinessSettings.business_id == business_id
    ).first()
    
    if not settings:
        # Create default settings
        settings = BusinessSettings(business_id=business_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings


@router.put("/businesses/{business_id}/settings", response_model=BusinessSettingsResponse)
def update_business_settings(
    business_id: int,
    update_data: BusinessSettingsUpdate,
    db: Session = Depends(get_db)
):
    """Update business settings"""
    settings = db.query(BusinessSettings).filter(
        BusinessSettings.business_id == business_id
    ).first()
    
    if not settings:
        settings = BusinessSettings(business_id=business_id)
        db.add(settings)
    
    # Update fields
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    return settings


@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
