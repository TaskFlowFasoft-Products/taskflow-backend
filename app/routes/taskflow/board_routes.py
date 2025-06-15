from fastapi import APIRouter, Depends, Path

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow.board import get_board_services
from app.interfaces.services.taskflow.board_services_interface import IBoardServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow.board_requests import CreateBoardRequest, BoardUpdateRequest
from app.schemas.responses.taskflow.board_responses import (
    GetBoardsResponse,
    BoardDeletionResponse,
    BoardCreatedResponse,
    BoardUpdateResponse
)

base_boards = APIRouter(
    prefix="/boards",
    tags=["TaskFlow Base - Boards"]
)


@base_boards.get("", response_model=GetBoardsResponse)
async def get_boards(
        user_data: UserJWTData = Depends(decode_access_token),
        board_services: IBoardServices = Depends(get_board_services)
) -> GetBoardsResponse:
    return await board_services.get_boards(user_data, ProductType.CORE)


@base_boards.delete("/{board_id}", response_model=BoardDeletionResponse)
async def delete_board(
        board_id: int = Path(title="ID do quadro.", description="ID do quadro a ser deletado."),
        user_data: UserJWTData = Depends(decode_access_token),
        board_services: IBoardServices = Depends(get_board_services)
) -> BoardDeletionResponse:
    return await board_services.delete_board(board_id, user_data)


@base_boards.post("", response_model=BoardCreatedResponse)
async def create_board(
        board_request: CreateBoardRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        board_services: IBoardServices = Depends(get_board_services)
) -> BoardCreatedResponse:
    return await board_services.create_board(board_request, user_data)


@base_boards.put("/{board_id}", response_model=BoardUpdateResponse)
async def update_board(
        board_request: BoardUpdateRequest,
        board_id: int = Path(title="ID do quadro.", description="ID do quadro a ser atualizado."),
        user_data: UserJWTData = Depends(decode_access_token),
        board_services: IBoardServices = Depends(get_board_services)
) -> BoardUpdateResponse:
    return await board_services.update_board(board_request, board_id, user_data)
