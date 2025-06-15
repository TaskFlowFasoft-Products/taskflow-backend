from fastapi import APIRouter, Depends, Path

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow.board import get_board_services
from app.dependencies.taskflow_gym.board import get_gym_board_services
from app.interfaces.services.taskflow.board_services_interface import IBoardServices
from app.interfaces.services.taskflow_gym.board_services_interface import IGymBoardServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow_gym.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse, GetBoardsResponse, BoardDeletionResponse
from app.schemas.responses.taskflow_gym.board_responses import GetGymBoardTemplatesResponse

gym_board = APIRouter(
    prefix="/gym/boards",
    tags=["TaskFlow Gym - Boards"]
)


@gym_board.get("/templates", response_model=GetGymBoardTemplatesResponse)
async def get_gym_board_templates(
    _user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymBoardServices = Depends(get_gym_board_services)
) -> GetGymBoardTemplatesResponse:
    return await gym_services.list_board_templates()


@gym_board.post("", response_model=BoardCreatedResponse)
async def add_gym_board_from_template(
    template: CreateBoardFromTemplateRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymBoardServices = Depends(get_gym_board_services)
) -> BoardCreatedResponse:
    return await gym_services.add_board_from_template(template, user_data)


@gym_board.get("", response_model=GetBoardsResponse)
async def get_user_gym_boards(
    user_data: UserJWTData = Depends(decode_access_token),
    board_services: IBoardServices = Depends(get_board_services)
) -> GetBoardsResponse:
    return await board_services.get_boards(user_data, product_type=ProductType.GYM)


@gym_board.delete("/{board_id}", response_model=BoardDeletionResponse)
async def delete_gym_board(
    user_data: UserJWTData = Depends(decode_access_token),
    board_id: int = Path(title="ID do Quadro", description="ID do quadro do Gym a ser deletado."),
    board_services: IBoardServices = Depends(get_board_services)
) -> BoardDeletionResponse:
    return await board_services.delete_board(board_id, user_data)
