from fastapi import Depends

from app.dependencies.taskflow.board import get_board_repository
from app.dependencies.taskflow.column import get_column_repository
from app.dependencies.taskflow.tasks import get_tasks_repository
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow.tasks_repository_interface import ITasksRepository
from app.interfaces.services.taskflow_movies.tasks_services_interface import IMoviesTasksServices
from app.services.taskflow_movies.tasks_services import MoviesTasksServices


def get_movies_tasks_services(
    tasks_repository: ITasksRepository = Depends(get_tasks_repository),
    board_repository: IBoardRepository = Depends(get_board_repository),
    column_repository: IColumnRepository = Depends(get_column_repository)
) -> IMoviesTasksServices:
    return MoviesTasksServices(tasks_repository, board_repository, column_repository)
