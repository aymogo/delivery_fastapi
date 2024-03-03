import datetime
from fastapi import APIRouter, status, HTTPException, Depends
from schemas import SignupModel, LoginModel
from database import session, engine
from models import User, Order, Product

# from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_


auth_router = APIRouter(prefix="/auth")
session = session(bind=engine)


@auth_router.get("/")
async def get_signup(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return {"message": "signup succes"}


# @auth_router.get("/signup")
# async def signup():
#     return


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    db_username = (
        session.query(User).filter(User.username == user.username).first()
    )
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)
    session.commit()
    data = {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "is_staff": new_user.is_staff,
        "is_active": new_user.is_active,
    }
    response_model = {
        "succes": True,
        "code": 201,
        "message": "user is created succesful",
        "data": data,
    }

    return response_model


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    # db_user = session.query(User).filter(User.username == user.username_or_email).first()

    db_user = (
        session.query(User)
        .filter(
            or_(
                User.username == user.username_or_email,
                User.email == user.username_or_email,
            )
        )
        .first()
    )

    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(
            subject=db_user.username, expires_time=access_lifetime
        )
        refresh_token = Authorize.create_refresh_token(
            subject=db_user.username, expires_time=refresh_lifetime
        )

        response = {"access": access_token, "refresh": refresh_token}

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password",
    )


@auth_router.get("/login/refresh")
async def regresh_roken(Authorize: AuthJWT = Depends()):
    try:
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=3)
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        db_user = (
            session.query(User).filter(User.username == current_user).first()
        )
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        new_access_token = Authorize.create_access_token(
            subject=db_user.username, expires_time=access_lifetime
        )

        response_model = {
            "succes": True,
            "code": 200,
            "message": "new access token is created",
            "data": {"accesss_token": new_access_token},
        }

        return response_model

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incalid refresh tokn",
        )
