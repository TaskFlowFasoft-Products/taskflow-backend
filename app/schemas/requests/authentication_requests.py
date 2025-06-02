from pydantic import BaseModel, EmailStr


class UserJWTData(BaseModel):
    email: EmailStr
    user_id: int


class UserRegistrationRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
