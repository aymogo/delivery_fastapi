from pydantic import BaseModel
from typing import Optional


class SignupModel(BaseModel):
    # id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@aa.aa",
                "password": "pass",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "2ea7ebd4ae708acad3cd8c549064bac58cfe368348ebb784ab3d097967ba4382"
    )


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    user_id: Optional[int]
    product_id: Optional[int]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "order_status": "PENDING"
            }
        }

class ProductModel(BaseModel):
    title: Optional[str]
    price: Optional[float]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "television",
                "price": 150.00
            }
        }