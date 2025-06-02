from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.services.board_services_interface import IBoardServices
from app.repository.board_repository import BoardRepository
from app.services.board_services import BoardServices


async def get_board_repository(session: AsyncSession = Depends(get_session)) -> IBoardRepository:
    return BoardRepository(session)


async def get_board_services(board_repository: IBoardRepository = Depends(get_board_repository)) -> IBoardServices:
    return BoardServices(board_repository)
