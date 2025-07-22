from typing import List
from fastapi import APIRouter
from starlette import status

from app.schemas.subscriptions import SubscriptionCreate, SubscriptionCreate, SubscriptionOutput, SubscriptionUpdate
from app.dependencies.database import db_dependency
from app.dependencies.auth import user_dependency
from app.services.subscriptions import create_subscriptions, list_user_subscriptions, delete_subscription, update_subscription

subscriptions_router = APIRouter(prefix='/subscriptions', tags=['subscriptions'])

@subscriptions_router.post("/", response_model=List[SubscriptionOutput], status_code=status.HTTP_201_CREATED)
def create_subscription_handler(subscriptions: List[SubscriptionCreate], db: db_dependency, user: user_dependency):
    return create_subscriptions(subscriptions, db, user)

@subscriptions_router.get("/", response_model=List[SubscriptionOutput], status_code=status.HTTP_200_OK)
def list_user_subscriptions_handler(db: db_dependency, user: user_dependency):
    return list_user_subscriptions(db, user)

@subscriptions_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription_handler(subscription_id: int, db: db_dependency, user: user_dependency):
    return delete_subscription(subscription_id, db, user)

@subscriptions_router.put("/{id}", response_model=SubscriptionCreate, status_code=status.HTTP_200_OK)
def update_subscription_handler(subscription_id: int, subscription: SubscriptionUpdate, db: db_dependency, user: user_dependency):
    return update_subscription(subscription_id, subscription, db, user)
