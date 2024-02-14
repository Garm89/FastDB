from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
import sqlalchemy

from sqlalchemy.orm import sessionmaker, relationship

from pydantic import BaseModel
from typing import List

DATABASE_URL = "sqlite:///./db.sqlite"

metadata = sqlalchemy.MetaData()


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Define SQLAlchemy models
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float

# Create tables in the database
metadata.create_all(bind=engine)

# Helper functions to work with the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI routes
@app.post("/users/", response_model=User)
async def create_user(user: User):
    db = next(get_db())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/", response_model=List[User])
async def get_users():
    db = next(get_db())
    return db.query(User).all()

@app.post("/orders/", response_model=Order)
async def create_order(order: Order):
    db = next(get_db())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/orders/", response_model=List[Order])
async def get_orders():
    db = next(get_db())
    return db.query(Order).all()

@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    db = next(get_db())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products/", response_model=List[Product])
async def get_products():
    db = next(get_db())
    return db.query(Product).all()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)