from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.requests.taskflow_movies.tasks_requests import (
    CreateMoviesTaskRequest,
    UpdateMoviesTaskRequest,
    DeleteMoviesTaskRequest
)
from app.schemas.responses.taskflow_movies.tasks_responses import (
    GetMoviesTasksResponse,
    CreateMoviesTaskResponse,
    UpdateMoviesTaskResponse
)


class IMoviesTasksServices(ABC):

    @abstractmethod
    async def create_task(self, request: CreateMoviesTaskRequest, user_data: UserJWTData) -> CreateMoviesTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def get_tasks_in_column(self, board_id: int, column_id: int, user_data: UserJWTData) -> GetMoviesTasksResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, request: UpdateMoviesTaskRequest, user_data: UserJWTData) -> UpdateMoviesTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, request: DeleteMoviesTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        raise NotImplementedError()
