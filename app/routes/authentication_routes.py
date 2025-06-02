from fastapi import APIRouter, Depends

from app.dependencies.authentication import get_auth_services
from app.interfaces.services.authentication_services_interface import IAuthenticationServices
from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse

authentication = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@authentication.post("/register", response_model=UserRegistrationResponse)
async def register_user(
        registration_data: UserRegistrationRequest,
        authentication_services: IAuthenticationServices = Depends(get_auth_services)
) -> UserRegistrationResponse:
    return await authentication_services.user_register(registration_data)


@authentication.post("/login", response_model=UserLoginResponse)
async def user_login(
        login_data: UserLoginRequest,
        authentication_services: IAuthenticationServices = Depends(get_auth_services)
) -> UserLoginResponse:
    return await authentication_services.user_login(login_data)
