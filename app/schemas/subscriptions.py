from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    name: str
    price: float
    installments: int

class SubscriptionCreate(SubscriptionBase):

    class Config:
        from_attributes = True

class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    installments: Optional[int] = None

class SubscriptionOutput(BaseModel):
    id: int
    name: str
    price: float
    installments: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
