from abc import ABC, abstractmethod

from pydantic import EmailStr

from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse


class IAuthenticationRepository(ABC):

    @abstractmethod
    async def email_already_registered(self, email: EmailStr) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def save_registration(self, registration_data: UserRegistrationRequest) -> UserRegistrationResponse:
        raise NotImplementedError()

    @abstractmethod
    async def verify_user_credentials(self, login_data: UserLoginRequest) -> UserLoginResponse:
        raise NotImplementedError()
