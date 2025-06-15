from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies.taskflow.board import get_board_repository
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow_gym.board_repository_interface import IGymBoardRepository
from app.interfaces.services.taskflow_gym.board_services_interface import IGymBoardServices
from app.repository.taskflow_gym.board_repository import GymBoardRepository
from app.services.taskflow_gym.board_services import GymBoardServices


def get_gym_board_repository(session: AsyncSession = Depends(get_session)) -> IGymBoardRepository:
    return GymBoardRepository(session)


def get_gym_board_services(
    gym_board_repository: IGymBoardRepository = Depends(get_gym_board_repository),
    board_repository: IBoardRepository = Depends(get_board_repository)
) -> IGymBoardServices:
    return GymBoardServices(gym_board_repository, board_repository)
