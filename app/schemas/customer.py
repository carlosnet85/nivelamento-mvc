from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from app.schemas.subscriptions import SubscriptionOutput

class CustomersBase(BaseModel):
    name: str
    email: EmailStr

class CustomerCreate(CustomersBase):
    password: str

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class CustomerOutput(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime] = None
    subscriptions: List[SubscriptionOutput]
    
    class Config:
        from_attributes = True