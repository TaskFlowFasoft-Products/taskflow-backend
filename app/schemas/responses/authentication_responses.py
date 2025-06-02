from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserRegistrationResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserLoginResponse(BaseModel):
    access_token: str
    expires_at: datetime
    username: str
