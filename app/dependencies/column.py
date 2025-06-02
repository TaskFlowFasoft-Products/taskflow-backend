from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.repository.column_repository_interface import IColumnRepository
from app.interfaces.services.column_services_interface import IColumnServices
from app.repository.board_repository import BoardRepository
from app.repository.column_repository import ColumnRepository
from app.services.column_services import ColumnServices


async def get_board_repository(session: AsyncSession = Depends(get_session)) -> IBoardRepository:
    return BoardRepository(session)


async def get_column_repository(session: AsyncSession = Depends(get_session)) -> IColumnRepository:
    return ColumnRepository(session)


async def get_column_services(
        column_repository: IColumnRepository = Depends(get_column_repository),
        board_repository: IBoardRepository = Depends(get_board_repository)
) -> IColumnServices:
    return ColumnServices(column_repository, board_repository)
