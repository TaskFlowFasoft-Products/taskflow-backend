from datetime import datetime

import pytest
from unittest.mock import AsyncMock
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient

from app.routes.authentication_routes import authentication
from app.dependencies.authentication import get_auth_services
from app.schemas.requests.authentication_requests import UserRegistrationRequest, UserLoginRequest
from app.schemas.responses.authentication_responses import UserRegistrationResponse, UserLoginResponse


@pytest.fixture
def app_with_routers():
    app = FastAPI()
    app.include_router(authentication)
    return app


@pytest.fixture
def client(app_with_routers):
    return TestClient(app_with_routers)


@pytest.fixture
def auth_service_mock():
    return AsyncMock()


@pytest.fixture(autouse=True)
def override_auth_service(app_with_routers, auth_service_mock):
    app_with_routers.dependency_overrides[get_auth_services] = lambda: auth_service_mock


@pytest.fixture
def registration_request():
    return UserRegistrationRequest(
        username="user1",
        email="user1@example.com",
        password="secret"
    )


@pytest.fixture
def registration_response():
    return UserRegistrationResponse(
        id=42,
        username="user1",
        email="user1@example.com",
        created_at=datetime(2025, 5, 18, 9, 30, 0)
    )


@pytest.fixture
def login_request():
    return UserLoginRequest(
        email="user1@example.com",
        password="secret"
    )


@pytest.fixture
def login_response():
    return UserLoginResponse(
        access_token="jwt-token-xyz",
        expires_at=datetime(2025, 5, 19, 9, 30, 0),
        username="user1"
    )


def test_register_success(client, auth_service_mock, registration_request, registration_response):
    auth_service_mock.user_register = AsyncMock(return_value=registration_response)

    resp = client.post("/auth/register", json=registration_request.model_dump())

    assert resp.status_code == 200
    assert resp.json() == {
        "id":  registration_response.id,
        "username":  registration_response.username,
        "email":  registration_response.email,
        "created_at":  registration_response.created_at.isoformat()
    }
    auth_service_mock.user_register.assert_called_once_with(registration_request)


def test_register_conflict(client, auth_service_mock, registration_request):
    auth_service_mock.user_register = AsyncMock(
        side_effect=HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado. Faça seu login ou insira um novo e-mail."
        )
    )

    resp = client.post("/auth/register", json=registration_request.model_dump())

    assert resp.status_code == 400
    assert resp.json() == {"detail": "Email já registrado. Faça seu login ou insira um novo e-mail."}
    auth_service_mock.user_register.assert_called_once_with(registration_request)


def test_login_success(client, auth_service_mock, login_request, login_response):
    auth_service_mock.user_login = AsyncMock(return_value=login_response)

    resp = client.post("/auth/login", json=login_request.model_dump())

    assert resp.status_code == 200
    assert resp.json() == {
        "access_token": login_response.access_token,
        "expires_at": login_response.expires_at.isoformat(),
        "username": login_response.username
    }
    auth_service_mock.user_login.assert_called_once_with(login_request)


def test_login_unauthorized(client, auth_service_mock, login_request):
    auth_service_mock.user_login = AsyncMock(
        side_effect=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falha ao autenticar. E-mail ou senha incorretos."
        )
    )

    resp = client.post("/auth/login", json=login_request.model_dump())

    assert resp.status_code == 401
    assert resp.json() == {"detail": "Falha ao autenticar. E-mail ou senha incorretos."}
    auth_service_mock.user_login.assert_called_once_with(login_request)
