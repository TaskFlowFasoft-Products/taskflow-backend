from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow.board_requests import CreateBoardRequest, BoardUpdateRequest
from app.schemas.responses.taskflow.board_responses import (
    GetBoardsResponse,
    BoardDeletionResponse,
    BoardCreatedResponse,
    BoardUpdateResponse
)


class IBoardServices(ABC):

    @abstractmethod
    async def get_boards(self, user_data: UserJWTData, product_type: ProductType) -> GetBoardsResponse:
        raise NotImplementedError()

    @abstractmethod
    async def delete_board(self, board_id: int, user_data: UserJWTData) -> BoardDeletionResponse:
        raise NotImplementedError()

    @abstractmethod
    async def create_board(self, board_request: CreateBoardRequest, user_data: UserJWTData) -> BoardCreatedResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update_board(
            self,
            board_request: BoardUpdateRequest,
            board_id: int,
            user_data: UserJWTData
    ) -> BoardUpdateResponse:
        raise NotImplementedError()
