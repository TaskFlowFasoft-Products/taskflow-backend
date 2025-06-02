from fastapi import HTTPException, status

from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.repository.column_repository_interface import IColumnRepository
from app.interfaces.services.column_services_interface import IColumnServices
from app.schemas.requests.authentication_requests import UserJWTData
from app.schemas.requests.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.column_responses import (
    CreateColumnResponse,
    DeleteColumnResponse,
    GetColumnsResponse,
    UpdateColumnResponse
)


class ColumnServices(IColumnServices):

    def __init__(self, column_repository: IColumnRepository, board_repository: IBoardRepository):
        self.column_repository = column_repository
        self.board_repository = board_repository

    async def create_column(self, column_request: CreateColumnRequest, user_data: UserJWTData) -> CreateColumnResponse:
        board_exists = await self.board_repository.check_board_existency(column_request.board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        column_info = await self.column_repository.create_column(column_request)

        return CreateColumnResponse(
            id=column_info.get("id"),
            title=column_request.title,
            board_id=column_request.board_id,
            created_at=column_info.get("created_at")
        )

    async def delete_column(self, column_request: DeleteColumnRequest, user_data: UserJWTData) -> DeleteColumnResponse:
        board_exists = await self.board_repository.check_board_existency(column_request.board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        await self.column_repository.delete_column(column_request)

        return DeleteColumnResponse(
            success=True,
            column_id=column_request.id,
            message="Coluna deletada com sucesso."
        )

    async def get_board_columns(self, board_id: int, user_data: UserJWTData) -> GetColumnsResponse:
        board_exists = await self.board_repository.check_board_existency(board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        columns = await self.column_repository.get_board_columns(board_id)

        return GetColumnsResponse(columns=columns)

    async def update_column(
            self,
            board_id: int,
            column_request: UpdateColumnRequest,
            user_data: UserJWTData
    ) -> UpdateColumnResponse:
        board_exists = await self.board_repository.check_board_existency(board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        update_info = await self.column_repository.update_column(board_id, column_request)

        return UpdateColumnResponse(
            success=True,
            id=column_request.column_id,
            message="Coluna atualizada com sucesso.",
            fields_updated=list(update_info.keys())
        )
