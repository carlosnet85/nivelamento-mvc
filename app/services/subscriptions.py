from typing import List
from fastapi import HTTPException
from sqlalchemy import func

from app.schemas.subscriptions import SubscriptionCreate, SubscriptionUpdate
from app.dependencies.database import db_dependency
from app.dependencies.auth import user_dependency
from app.models.customer import Customer
from app.models.subscriptions import Subscription

def list_user_subscriptions(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    return db.query(Subscription).filter(Subscription.customer_id == user["id"]).all()

def create_subscriptions(subscriptions: List[SubscriptionCreate], db: db_dependency, user: user_dependency):
    db_subscriptions = []

    if user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    if not subscriptions:
        raise HTTPException(status_code=400, detail="No subscriptions provided")
    if not isinstance(subscriptions, list):
        raise HTTPException(status_code=400, detail="Subscriptions must be a list")
    
    for sub in subscriptions:
        new_subscription = Subscription(
            name=sub.name,
            customer_id=user["id"],
            price=sub.price,
            installments=sub.installments
        )

        db.add(new_subscription)
        db_subscriptions.append(new_subscription)
        db.commit()
    
    db.commit()
    
            
    for sub in db_subscriptions:
        db.refresh(sub)
    return db_subscriptions

def delete_subscription(subscription_id: int, db: db_dependency, user: user_dependency):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()

    if user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    if not subscription:
        raise HTTPException(status_code=400, detail="No subscription provided")
    
    db.delete(subscription)
    db.commit()
    return subscription

def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: db_dependency, user: user_dependency):
    subscriptions = db.query(Subscription).filter(Subscription.id == subscription_id).first()

    if user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    if not subscriptions:
        raise HTTPException(status_code=400, detail="No subscriptions provided")
    
    update_data = subscription.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(subscriptions, key, value)
    db.commit()
    db.refresh(subscriptions)
    return subscriptions