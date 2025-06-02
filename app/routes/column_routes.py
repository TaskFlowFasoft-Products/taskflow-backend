from fastapi import APIRouter, Depends, Path

from app.core.jwt_auth import decode_access_token
from app.dependencies.column import get_column_services
from app.interfaces.services.column_services_interface import IColumnServices
from app.schemas.requests.authentication_requests import UserJWTData
from app.schemas.requests.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.column_responses import (
    CreateColumnResponse,
    DeleteColumnResponse,
    GetColumnsResponse,
    UpdateColumnResponse
)

column = APIRouter(
    prefix="/column",
    tags=["Column"]
)


@column.post("", response_model=CreateColumnResponse)
async def create_column(
        column_request: CreateColumnRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> CreateColumnResponse:
    return await column_services.create_column(column_request, user_data)


@column.delete("", response_model=DeleteColumnResponse)
async def delete_column(
        column_request: DeleteColumnRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> DeleteColumnResponse:
    return await column_services.delete_column(column_request, user_data)


@column.get("/{board_id}", response_model=GetColumnsResponse)
async def get_board_columns(
        board_id: int = Path(title="ID do quadro.", description="ID do quadro cujas colunas serão retornadas."),
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> GetColumnsResponse:
    return await column_services.get_board_columns(board_id, user_data)


@column.put("/{board_id}", response_model=UpdateColumnResponse)
async def update_column(
        column_request: UpdateColumnRequest,
        board_id: int = Path(title="ID do quadro.", description="ID do quadro cujas colunas serão atualizadas."),
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> UpdateColumnResponse:
    return await column_services.update_column(board_id, column_request, user_data)
