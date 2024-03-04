from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth.auth_jwt import AuthJWT
from models import User, Order, Product
from schemas import OrderModel, OrderStatusModel, ProductModel
from database import session, engine

product_router = APIRouter(prefix="/product")
session = session(bind=engine)


@product_router.get("/list", status_code=status.HTTP_200_OK)
async def product_list(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access toiken",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        products = session.query(Product).all()
        return jsonable_encoder(products)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't access for this page",
        )


@product_router.post("/create", status_code=status.HTTP_201_CREATED)
async def product_create(product: ProductModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access toiken",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()
    if current_user.is_staff:
        new_product = Product(
            title=product.title,
            price=product.price,
        )
        if (
            not session.query(Product)
            .filter(Product.title == new_product.title)
            .first()
        ):
            session.add(new_product)
            session.commit()
            data = {
                "success": True,
                "code": 201,
                "message": "Product is created successfully",
                "data": {
                    "id": new_product.id,
                    "title": new_product.title,
                    "price": new_product.price,
                },
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product with this title already exists",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't access for this page",
        )


@product_router.get("/{id}")
async def get_product_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter a valid access token",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        return jsonable_encoder(product)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't acces for this page",
        )


@product_router.delete("/{id}/update", status_code=status.HTTP_204_NO_CONTENT)
async def deleete_product_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access token",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            session.delete(product)
            session.commit()
            data = {
                "success": True,
                "code": 200,
                "message": f"product with ID {id} has been deleted",
                "data": None,
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product with ID {id} is not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't access for delete",
        )


@product_router.put("/{id}/update", status_code=status.HTTP_200_OK)
async def update_product_by_id(
    id: int, update_data: ProductModel, Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter a valid access token",
        )

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        product = session.query(Product).filter(Product.id == id).first()
        if product:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(product, key, value)

            session.commit()
            data = {
                "success": True,
                "code": 200,
                "message": f"product with ID {id} has been updated",
                "data": {
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                },
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product with ID {id} is not found",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you haven't access for update",
        )
