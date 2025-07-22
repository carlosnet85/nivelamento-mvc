from fastapi import APIRouter
from starlette import status
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOutput
from app.dependencies.database import db_dependency
from app.dependencies.auth import user_dependency
from app.services.customer import get_customer_info, create_customer, update_customer, delete_customer

customers_router = APIRouter(prefix='/customers', tags=['customers'])

@customers_router.get("/", response_model=CustomerOutput, status_code=status.HTTP_200_OK)
def get_customer_info_handler(db: db_dependency, user: user_dependency):
    return get_customer_info(db, user)

@customers_router.post("/", response_model=CustomerOutput, status_code=status.HTTP_201_CREATED)
def create_customer_handler(customer: CustomerCreate, db: db_dependency):
    return create_customer(db, customer)

@customers_router.put("/", response_model=CustomerOutput, status_code=status.HTTP_200_OK)
def update_customer_handler(user: user_dependency, db: db_dependency, customer_data: CustomerUpdate):
    return update_customer(user, db, customer_data)

@customers_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_handler(user: user_dependency, db: db_dependency):
    return delete_customer(user, db)