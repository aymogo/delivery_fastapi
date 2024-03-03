from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth.auth_jwt import AuthJWT
from models import User, Order, Product
from schemas import OrderModel, OrderStatusModel
from database import session, engine

order_router = APIRouter(prefix="/order")
session = session(bind=engine)


@order_router.get("/")
async def get_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access toiken",
        )

    return {"message": "get order page"}


@order_router.post("/make", status_code=status.HTTP_201_CREATED)
async def maek_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access toiken",
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email == current_user).first()

    new_order = Order(
        quantity=order.quantity,
        # order_status=order.order_status,
        # user_id=order.user_id,
        # product_id=order.product_id,
    )

    session.add(new_order)
    session.commit()

    response = {
        "id": new_order.id,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status,
        "product": new_order.product,
    }

    return jsonable_encoder(response)


@order_router.get("/list")
async def list_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter a valid access token",
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't acces for this page",
        )
