from abc import ABC, abstractmethod
from typing import List

from app.schemas.requests.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.column_responses import Column


class IColumnRepository(ABC):

    @abstractmethod
    async def create_column(self, column_request: CreateColumnRequest) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def check_column_existency(self, column_id: int, board_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_column(self, column_request: DeleteColumnRequest):
        raise NotImplementedError()

    @abstractmethod
    async def get_board_columns(self, board_id: int) -> List[Column]:
        raise NotImplementedError()

    @abstractmethod
    async def update_column(self, board_id: int, column_request: UpdateColumnRequest) -> dict:
        raise NotImplementedError()
