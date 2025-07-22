from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.dependencies.auth import user_dependency
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.core.auth import bcrypt_context, get_password_hash

def get_customer_by_id(user: user_dependency, db: Session):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return db.query(Customer).filter(Customer.id == user["id"]).first()

def get_customer_info(db: Session, user: user_dependency):
    return get_customer_by_id(user, db)

def create_customer(db: Session, customer: CustomerCreate):
    password = get_password_hash(customer.password)
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        password=password
    )
    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    return db_customer


def update_customer(user: user_dependency, db: Session, customer_data: CustomerUpdate):
    db_customer = get_customer_by_id(user, db)

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = customer_data.model_dump(exclude_unset=True)

    new_password = update_data.pop("password", None)
    if new_password:
        setattr(db_customer, "password", bcrypt_context.hash(new_password))

    for field, value in update_data.items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(user: user_dependency, db: Session):
    db_customer = get_customer_by_id(user, db)

    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return db_customer
