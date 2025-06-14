from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.dependencies.taskflow.board import get_board_repository
from app.dependencies.taskflow.column import get_column_repository
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow_studies.board_repository_interface import IBoardStudiesRepository
from app.interfaces.services.taskflow_studies.board_services_interface import IBoardStudiesServices
from app.repository.taskflow_studies.board_repository import BoardStudiesRepository
from app.services.taskflow_studies.board_services import BoardStudiesServices


async def get_studies_board_repository(session: AsyncSession = Depends(get_session)) -> IBoardStudiesRepository:
    return BoardStudiesRepository(session)


async def get_studies_board_services(
    studies_repository: IBoardStudiesRepository = Depends(get_studies_board_repository),
    board_repository: IBoardRepository = Depends(get_board_repository),
    column_repository: IColumnRepository = Depends(get_column_repository)
) -> IBoardStudiesServices:
    return BoardStudiesServices(studies_repository, board_repository, column_repository)
