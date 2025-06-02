from abc import ABC, abstractmethod

from app.schemas.requests.authentication_requests import UserJWTData
from app.schemas.requests.tasks_requests import CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest
from app.schemas.responses.tasks_responses import (
    CreateTaskResponse,
    GetColumnTasksResponse,
    DeleteTaskResponse,
    UpdateTaskResponse
)


class ITasksServices(ABC):

    @abstractmethod
    async def create_task(self, tasks_request: CreateTaskRequest, user_data: UserJWTData) -> CreateTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def get_column_tasks(self, column_id: int, board_id: int, user_data: UserJWTData) -> GetColumnTasksResponse:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, tasks_request: DeleteTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, tasks_request: UpdateTaskRequest, user_data: UserJWTData) -> UpdateTaskResponse:
        raise NotImplementedError()
