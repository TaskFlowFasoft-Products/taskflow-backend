from fastapi import APIRouter, Depends, Path

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow.board import get_board_services
from app.dependencies.taskflow_movies.board import get_movies_board_services
from app.interfaces.services.taskflow.board_services_interface import IBoardServices
from app.interfaces.services.taskflow_movies.board_services_interface import IMoviesBoardServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow_movies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse, GetBoardsResponse, BoardDeletionResponse
from app.schemas.responses.taskflow_movies.board_responses import GetMoviesBoardTemplatesResponse

movies_board = APIRouter(
    prefix="/movies/boards",
    tags=["TaskFlow Movies - Boards"]
)


@movies_board.get("/templates", response_model=GetMoviesBoardTemplatesResponse)
async def get_movies_board_templates(
    _user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesBoardServices = Depends(get_movies_board_services)
) -> GetMoviesBoardTemplatesResponse:
    return await movies_services.list_board_templates()


@movies_board.post("", response_model=BoardCreatedResponse)
async def add_movies_board_from_template(
    template: CreateBoardFromTemplateRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesBoardServices = Depends(get_movies_board_services)
) -> BoardCreatedResponse:
    return await movies_services.add_board_from_template(template, user_data)


@movies_board.get("", response_model=GetBoardsResponse)
async def get_user_movies_boards(
    user_data: UserJWTData = Depends(decode_access_token),
    board_services: IBoardServices = Depends(get_board_services)
) -> GetBoardsResponse:
    return await board_services.get_boards(user_data, product_type=ProductType.MOVIES)


@movies_board.delete("/{board_id}", response_model=BoardDeletionResponse)
async def delete_movies_board(
    user_data: UserJWTData = Depends(decode_access_token),
    board_id: int = Path(title="ID do Quadro", description="ID do quadro do movies a ser deletado."),
    board_services: IBoardServices = Depends(get_board_services)
) -> BoardDeletionResponse:
    return await board_services.delete_board(board_id, user_data)
