from fastapi import FastAPI

from app.controllers.auth import auth_router
from app.controllers.customers import customers_router
from app.controllers.subscriptions import subscriptions_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(subscriptions_router)