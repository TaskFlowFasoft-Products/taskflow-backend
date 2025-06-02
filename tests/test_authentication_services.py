import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from fastapi import HTTPException, status

from app.services.authentication_services import AuthenticationServices
from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse


@pytest.fixture
def registration_request():
    return UserRegistrationRequest(
        username="user1",
        email="user1@example.com",
        password="secret",
    )


@pytest.fixture
def registration_response():
    return UserRegistrationResponse(
        id=1,
        username="user1",
        email="user1@example.com",
        created_at=datetime(2025, 5, 18, 0, 0, 0),
    )


@pytest.fixture
def login_request():
    return UserLoginRequest(
        email="user1@example.com",
        password="secret",
    )


@pytest.fixture
def login_response():
    return UserLoginResponse(
        access_token="token-123",
        expires_at=datetime(2025, 5, 19, 0, 0, 0),
        username="user1"
    )


@pytest.fixture
def authentication_repository_mock():
    return AsyncMock()


@pytest.mark.asyncio
async def test_user_register_success(authentication_repository_mock, registration_request, registration_response):
    authentication_repository_mock.email_already_registered.return_value = False
    authentication_repository_mock.save_registration.return_value = registration_response

    authentication_services = AuthenticationServices(authentication_repository_mock)
    result = await authentication_services.user_register(registration_request)

    assert result == registration_response
    authentication_repository_mock.email_already_registered.assert_awaited_once_with(registration_request.email)
    authentication_repository_mock.save_registration.assert_awaited_once_with(registration_request)


@pytest.mark.asyncio
async def test_user_register_conflict(authentication_repository_mock, registration_request):
    authentication_repository_mock.email_already_registered.return_value = True

    authentication_services = AuthenticationServices(authentication_repository_mock)

    with pytest.raises(HTTPException) as exc:
        await authentication_services.user_register(registration_request)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email já registrado" in exc.value.detail
    authentication_repository_mock.email_already_registered.assert_awaited_once_with(registration_request.email)
    authentication_repository_mock.save_registration.assert_not_called()


@pytest.mark.asyncio
async def test_user_login_success(authentication_repository_mock, login_request, login_response):
    authentication_repository_mock.verify_user_credentials.return_value = login_response

    authentication_services = AuthenticationServices(authentication_repository_mock)
    result = await authentication_services.user_login(login_request)

    assert result == login_response
    authentication_repository_mock.verify_user_credentials.assert_awaited_once_with(login_request)


@pytest.mark.asyncio
async def test_user_login_unauthorized(authentication_repository_mock, login_request):
    authentication_repository_mock.verify_user_credentials.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Falha ao autenticar. E-mail ou senha incorretos."
    )

    authentication_services = AuthenticationServices(authentication_repository_mock)

    with pytest.raises(HTTPException) as exc:
        await authentication_services.user_login(login_request)

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    authentication_repository_mock.verify_user_credentials.assert_awaited_once_with(login_request)
