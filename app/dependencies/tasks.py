from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.repository.column_repository_interface import IColumnRepository
from app.interfaces.repository.tasks_repository_interface import ITasksRepository
from app.interfaces.services.tasks_services_interface import ITasksServices
from app.repository.board_repository import BoardRepository
from app.repository.column_repository import ColumnRepository
from app.repository.tasks_repository import TasksRepository
from app.services.tasks_services import TasksServices


async def get_board_repository(session: AsyncSession = Depends(get_session)) -> IBoardRepository:
    return BoardRepository(session)


async def get_column_repository(session: AsyncSession = Depends(get_session)) -> IColumnRepository:
    return ColumnRepository(session)


async def get_tasks_repository(session: AsyncSession = Depends(get_session)) -> ITasksRepository:
    return TasksRepository(session)


async def get_tasks_services(
        column_repository: IColumnRepository = Depends(get_column_repository),
        board_repository: IBoardRepository = Depends(get_board_repository),
        tasks_repository: ITasksRepository = Depends(get_tasks_repository)
) -> ITasksServices:
    return TasksServices(column_repository, board_repository, tasks_repository)
