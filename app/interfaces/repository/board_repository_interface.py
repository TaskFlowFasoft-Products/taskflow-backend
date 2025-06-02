from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.requests.board_requests import BoardUpdateRequest
from app.schemas.responses.board_responses import Board


class IBoardRepository(ABC):

    @abstractmethod
    async def check_board_existency(self, board_id: int, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_boards(self, user_id: int) -> Optional[List[Board]]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_board(self, board_id: int, user_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def create_board(self, title: str, user_id: int) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def update_board(
            self,
            board_request: BoardUpdateRequest,
            board_id: int,
            user_id: int
    ) -> dict:
        raise NotImplementedError()
