from abc import ABC, abstractmethod

from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse


class IAuthenticationServices(ABC):

    @abstractmethod
    async def user_register(self, registration_data: UserRegistrationRequest) -> UserRegistrationResponse:
        raise NotImplementedError()

    @abstractmethod
    async def user_login(self, login_data: UserLoginRequest) -> UserLoginResponse:
        raise NotImplementedError()
