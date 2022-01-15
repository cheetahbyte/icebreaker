from urllib.request import Request
from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
import typing
from datetime import timedelta, datetime
from jose import jwt, JWTError
from core.config import Config

# orm
from orm.models import User

# utils
from jose import jwt, JWTError

# config
from core.config import Config

# models
from dto.user import TokenData, CurrentUser


def create_access_token(
    payload: dict, expires: typing.Optional[timedelta] = None
) -> str:
    to_encode: dict = payload.copy()
    if expires:
        expire = datetime.utcnow() + expires
    else:
        ## TODO: settings
        expire = datetime.utcnow() + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRES)
    to_encode.update({"exp": expire})
    ## TODO: add secret
    encoded_jwt = jwt.encode(
        to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM
    )
    return encoded_jwt


# dependencies for jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(sub=sub)
    except JWTError as e:
        raise credentials_exception
    user = await User.get(username=token_data.sub)
    if user is None:
        raise credentials_exception
    return CurrentUser(**{"id": user.id, "name": user.username, "admin": user.admin})


async def current_user_is_admin(current_user: CurrentUser = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin only endpoint"
        )
    return current_user


async def has_container_perms(id, current_user: CurrentUser = Depends(get_current_user)):
    # TODO: add permissions checks for group and user
    if current_user.admin:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )
