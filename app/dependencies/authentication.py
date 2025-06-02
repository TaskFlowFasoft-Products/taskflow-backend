from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.interfaces.repository.authentication_repository_interface import IAuthenticationRepository
from app.interfaces.services.authentication_services_interface import IAuthenticationServices
from app.repository.authentication_repository import AuthenticationRepository
from app.services.authentication_services import AuthenticationServices


async def get_auth_repository(session: AsyncSession = Depends(get_session)) -> IAuthenticationRepository:
    return AuthenticationRepository(session)


async def get_auth_services(
        auth_repository: IAuthenticationRepository = Depends(get_auth_repository)
) -> IAuthenticationServices:
    return AuthenticationServices(auth_repository)
