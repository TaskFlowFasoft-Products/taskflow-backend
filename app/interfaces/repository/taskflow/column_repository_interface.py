from abc import ABC, abstractmethod
from typing import List, Dict

from app.schemas.requests.taskflow.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.taskflow.column_responses import Column


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

    @abstractmethod
    async def create_columns_in_batch(self, board_id: int, columns: List[Dict]):
        raise NotImplementedError()
