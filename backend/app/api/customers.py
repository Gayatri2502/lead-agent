"""Customer endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas import CustomerCreate, CustomerUpdate, CustomerResponse
from app.models import Customer, Business

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    business_id: int,
    skip: int = Query(0),
    limit: int = Query(100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """List customers for a business"""
    query = db.query(Customer).filter(Customer.business_id == business_id)
    
    if search:
        query = query.filter(
            (Customer.name.ilike(f"%{search}%")) |
            (Customer.phone.ilike(f"%{search}%")) |
            (Customer.email.ilike(f"%{search}%"))
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get customer details"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    return customer


@router.post("/", response_model=CustomerResponse)
def create_customer(
    business_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Create new customer"""
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Business not found")
    
    # Check if customer already exists
    existing = db.query(Customer).filter(
        Customer.business_id == business_id,
        Customer.phone == customer_data.phone
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Customer with this phone already exists"
        )
    
    # Create customer
    customer = Customer(
        business_id=business_id,
        **customer_data.dict()
    )
    
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    update_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    """Update customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    # Update fields
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    
    return {"message": "Customer deleted"}
