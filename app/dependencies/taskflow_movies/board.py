from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies.taskflow.board import get_board_repository
from app.dependencies.taskflow.column import get_column_repository
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow_movies.board_repository_interface import IMoviesBoardRepository
from app.interfaces.services.taskflow_movies.board_services_interface import IMoviesBoardServices
from app.repository.taskflow_movies.board_repository import MoviesBoardRepository
from app.services.taskflow_movies.board_services import MoviesBoardServices


async def get_movies_board_repository(session: AsyncSession = Depends(get_session)) -> IMoviesBoardRepository:
    return MoviesBoardRepository(session)


async def get_movies_board_services(
    movies_board_repository: IMoviesBoardRepository = Depends(get_movies_board_repository),
    board_repository: IBoardRepository = Depends(get_board_repository),
    column_repository: IColumnRepository = Depends(get_column_repository)
) -> IMoviesBoardServices:
    return MoviesBoardServices(movies_board_repository, board_repository, column_repository)
