from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth.auth_jwt import AuthJWT
from models import User, Order, Product
from schemas import OrderModel, OrderStatusModel
from database import session, engine

order_router = APIRouter(prefix="/order")
session = session(bind=engine)


@order_router.get("/")
async def get_order(
    Authorize: AuthJWT = Depends(), status_code=status.HTTP_200_OK
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access toiken",
        )

    return {"message": "get order page"}


@order_router.post("/create", status_code=status.HTTP_201_CREATED)
async def make_order(
    order: OrderModel,
    Authorize: AuthJWT = Depends(),
    status_code=status.HTTP_200_OK,
):
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
        product_id=order.product_id,
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "id": new_order.id,
        "product": {
            "id": new_order.product.id,
            "title": new_order.product.title,
            "price": new_order.product.price,
        },
        "quantity": new_order.quantity,
        "order_status": new_order.order_status.value,
        "total_price": new_order.quantity * new_order.product.price,
    }

    return jsonable_encoder(response)


@order_router.get("/list")
async def order_list(
    Authorize: AuthJWT = Depends(), status_code=status.HTTP_200_OK
):
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
        custom_data = [
            {
                "id": order.id,
                "user": {
                    "id": order.user.id,
                    "username": order.user.username,
                    "email": order.user.email,
                },
                "product": {
                    "id": order.product.id,
                    "title": order.product.title,
                    "price": order.product.price,
                },
                "quantity": order.quantity,
                "order_status": order.order_status.value,
                "total_price": order.quantity * order.product.price,
            }
            for order in orders
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't access for this page",
        )


@order_router.get("/{id}")
async def get_order_by_id(
    id: int, Authorize: AuthJWT = Depends(), status_code=status.HTTP_200_OK
):
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
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            custom_order = {
                "id": order.id,
                "user": {
                    "id": order.user.id,
                    "username": order.user.username,
                    "mail": order.user.email,
                },
                "product": {
                    "id": order.product.id,
                    "title": order.product.title,
                    "price": order.product.price,
                },
                "quantity": order.quantity,
                "order_status": order.order_status.value,
                "total_price": order.quantity * order.product.price,
            }
        return jsonable_encoder(custom_order)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't acces for this page",
        )


@order_router.get("/user/orders")
async def get_user_orders(
    Authorize: AuthJWT = Depends(), status_code=status.HTTP_200_OK
):
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
        custom_data = [
            {
                "id": order.id,
                "user": {
                    "id": order.user.id,
                    "username": order.user.username,
                    "email": order.user.email,
                },
                "product": {
                    "id": order.product.id,
                    "title": order.product.title,
                    "price": order.product.price,
                },
                "quantity": order.quantity,
                "order_status": order.order_status.value,
                "total_price": order.quantity * order.product.price,
            }
            for order in user.orders
        ]
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't acces for this page",
        )


@order_router.get("/user/orders/{id}", status_code=status.HTTP_200_OK)
async def get_user_order_by_id(id: int, Authorize: AuthJWT = Depends()):
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
        order = session.query(Order).filter(Order.id == id).first()
        custom_data = {
            "id": order.id,
            "user": {
                "id": order.user.id,
                "username": order.user.username,
                "email": order.user.email,
            },
            "product": {
                "id": order.product.id,
                "title": order.product.title,
                "price": order.product.price,
            },
            "quantity": order.quantity,
            "order_status": order.order_status.value,
            "total_price": order.quantity * order.product.price,
        }
        return jsonable_encoder(custom_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't acces for this page",
        )


@order_router.put('/{id}/update', status_code=status.HTTP_200_OK)
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter a valid access token",
        )

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    update_order = session.query(Order).filter(Order.id == id).first()
    if update_order.user != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you cannot update other's orders",
        )
    
    update_order.quantity = order.quantity 
    update_order.product_id = order.product_id 
    session.commit()

    custom_data = {
        "success": True,
        "code": 200,
        "message": "order has been successfuly updated",
        "data": {
            "id": update_order.id,
            "quantity": update_order.quantity,
            "product_id": update_order.product_id,
            "order_status": update_order.order_status,
        }
    }

    return jsonable_encoder(custom_data)


