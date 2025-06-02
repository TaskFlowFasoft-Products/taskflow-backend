from typing import Optional

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.services.board_services_interface import IBoardServices
from app.schemas.requests.board_requests import CreateBoardRequest, BoardUpdateRequest
from app.schemas.responses.board_responses import (
    GetBoardsResponse,
    BoardDeletionResponse,
    BoardCreatedResponse,
    BoardUpdateResponse
)


class BoardServices(IBoardServices):

    def __init__(self, board_repository: IBoardRepository):
        self.board_repository = board_repository

    async def get_boards(self, user_data: UserJWTData) -> Optional[GetBoardsResponse]:
        boards = await self.board_repository.get_user_boards(user_data.user_id)

        return GetBoardsResponse(boards=boards)

    async def delete_board(self, board_id: int, user_data: UserJWTData) -> BoardDeletionResponse:
        await self.board_repository.delete_board(board_id, user_data.user_id)

        return BoardDeletionResponse(
            success=True,
            board_id=board_id,
            message=f"Quadro deletado com sucesso."
        )

    async def create_board(self, board_request: CreateBoardRequest, user_data: UserJWTData) -> BoardCreatedResponse:
        board_info = await self.board_repository.create_board(board_request.title, user_data.user_id)

        return BoardCreatedResponse(
            board_id=board_info.get("id"),
            message="Quadro criado com sucesso.",
            created_at=board_info.get("created_at")
        )

    async def update_board(
            self,
            board_request: BoardUpdateRequest,
            board_id: int,
            user_data: UserJWTData
    ) -> BoardUpdateResponse:
        update_info = await self.board_repository.update_board(board_request, board_id, user_data.user_id)

        return BoardUpdateResponse(
            success=True,
            board_id=board_id,
            message="Quadro atualizado com sucesso.",
            fields_updated=list(update_info.keys())
        )
