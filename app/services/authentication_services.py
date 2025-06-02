from fastapi import HTTPException, status

from app.interfaces.repository.authentication_repository_interface import IAuthenticationRepository
from app.interfaces.services.authentication_services_interface import IAuthenticationServices
from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse


class AuthenticationServices(IAuthenticationServices):

    def __init__(self, auth_repository: IAuthenticationRepository):
        self.auth_repository = auth_repository

    async def user_register(self, registration_data: UserRegistrationRequest) -> UserRegistrationResponse:
        email_not_available = await self.auth_repository.email_already_registered(registration_data.email)

        if email_not_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado. Faça seu login ou insira um novo e-mail."
            )

        user_registration = await self.auth_repository.save_registration(registration_data)

        return user_registration

    async def user_login(self, login_data: UserLoginRequest) -> UserLoginResponse:
        login = await self.auth_repository.verify_user_credentials(login_data)

        return login
