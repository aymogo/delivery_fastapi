from database import Base
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    Text,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(70), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")  # one to many

    def __repr__(self):
        return f"<user {self.id}"


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN_TRANSIT", "in_transit"),
        ("DELIVERED", "delivered"),
    )

    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="orders")
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return f"<oder {self.id}>"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    price = Column(Integer)
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"<product {self.title}>"
