from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.requests.taskflow_gym.tasks_requests import CreateGymTaskRequest, UpdateGymTaskRequest, DeleteGymTaskRequest
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.responses.taskflow_gym.tasks_responses import GetGymTasksResponse, CreateGymTaskResponse, UpdateGymTaskResponse


class IGymTasksServices(ABC):

    @abstractmethod
    async def create_task(self, request: CreateGymTaskRequest, user_data: UserJWTData) -> CreateGymTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def get_tasks_in_column(self, board_id: int, column_id: int, user_data: UserJWTData) -> GetGymTasksResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, request: UpdateGymTaskRequest, user_data: UserJWTData) -> UpdateGymTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, request: DeleteGymTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        raise NotImplementedError()
