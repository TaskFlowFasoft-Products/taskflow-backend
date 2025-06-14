from fastapi import APIRouter, Depends, Path

from app.core.jwt_auth import decode_access_token
from app.dependencies.taskflow.column import get_column_services
from app.interfaces.services.taskflow.column_services_interface import IColumnServices
from app.schemas.requests.authentication_requests import UserJWTData
from app.schemas.requests.taskflow.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.taskflow.column_responses import (
    CreateColumnResponse,
    DeleteColumnResponse,
    GetColumnsResponse,
    UpdateColumnResponse
)

base_column = APIRouter(
    prefix="/column",
    tags=["TaskFlow Base - Column"]
)


@base_column.post("", response_model=CreateColumnResponse)
async def create_column(
        column_request: CreateColumnRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> CreateColumnResponse:
    return await column_services.create_column(column_request, user_data)


@base_column.delete("", response_model=DeleteColumnResponse)
async def delete_column(
        column_request: DeleteColumnRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> DeleteColumnResponse:
    return await column_services.delete_column(column_request, user_data)


@base_column.get("/{board_id}", response_model=GetColumnsResponse)
async def get_board_columns(
        board_id: int = Path(title="ID do quadro.", description="ID do quadro cujas colunas serão retornadas."),
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> GetColumnsResponse:
    return await column_services.get_board_columns(board_id, user_data)


@base_column.put("/{board_id}", response_model=UpdateColumnResponse)
async def update_column(
        column_request: UpdateColumnRequest,
        board_id: int = Path(title="ID do quadro.", description="ID do quadro cujas colunas serão atualizadas."),
        user_data: UserJWTData = Depends(decode_access_token),
        column_services: IColumnServices = Depends(get_column_services)
) -> UpdateColumnResponse:
    return await column_services.update_column(board_id, column_request, user_data)
