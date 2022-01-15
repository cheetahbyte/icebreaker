from sys import prefix
from fastapi import APIRouter
from fastapi import responses
from fastapi import Depends

# orm
from orm.models import User
import tortoise.exceptions

# dto
from dto.user import CurrentUser, UserCreateDTO, UserLoginDTO

# bcrypt
import bcrypt

# core
from core.security import get_current_user, current_user_is_admin, create_access_token

router = APIRouter(tags=["user"])


@router.post("/")
async def create_user(
    data: UserCreateDTO, admin: CurrentUser = Depends(current_user_is_admin)
) -> dict:
    """create user"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data.password.encode(), salt)
    data.password = hashed_password.decode()
    try:
        user = await User.create(**data.dict())
        return {"sub": user.id, "name": user.username}
    except (tortoise.exceptions.IntegrityError) as e:
        # user already exists
        return responses.JSONResponse(
            status_code=409, content={"error": "user already exists", "message": str(e)}
        )


auth_router = APIRouter(tags=["auth"])


@auth_router.post("/login")
async def login(data: UserLoginDTO) -> dict:
    """login user"""
    try:
        user = await User.get(username=data.username)
        if bcrypt.checkpw(data.password.encode(), user.password.encode()):
            payload = {"id": user.id, "sub": user.username, "admin": user.admin}
            return {"access_token": create_access_token(payload)}
        else:
            return responses.JSONResponse(
                status_code=401, content={"error": "invalid password"}
            )
    except (tortoise.exceptions.DoesNotExist) as e:
        return responses.JSONResponse(
            status_code=401, content={"error": "invalid username"}
        )


me_router = APIRouter(tags=["me"])


@me_router.get("/")
async def get_me(user=Depends(get_current_user)) -> dict:
    return user


router.include_router(me_router, prefix="/@me")

router.include_router(auth_router, prefix="/auth")
