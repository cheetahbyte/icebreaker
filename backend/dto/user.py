import pydantic


class UserCreateDTO(pydantic.BaseModel):
    username: str
    password: str
    admin: bool = False

class UserLoginDTO(pydantic.BaseModel):
    username: str
    password: str

class TokenData(pydantic.BaseModel):
    sub: str 


class CurrentUser(pydantic.BaseModel):
    id: str
    name: str
    admin: bool