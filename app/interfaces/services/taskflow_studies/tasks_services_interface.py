from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.requests.taskflow.tasks_requests import DeleteTaskRequest
from app.schemas.requests.taskflow_studies.tasks_requests import CreateStudiesTaskRequest, UpdateStudiesTaskRequest
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.responses.taskflow_studies.tasks_responses import (
    GetStudiesTasksResponse,
    CreateStudiesTaskResponse,
    UpdateStudiesTaskResponse
)


class IStudiesTasksServices(ABC):

    @abstractmethod
    async def create_task(
            self,
            tasks_request: CreateStudiesTaskRequest,
            user_data: UserJWTData
    ) -> CreateStudiesTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def get_tasks_in_column(
            self,
            board_id: int,
            column_id: int,
            user_data: UserJWTData
    ) -> GetStudiesTasksResponse:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, tasks_request: DeleteTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(
            self,
            tasks_request: UpdateStudiesTaskRequest,
            user_data: UserJWTData
    ) -> UpdateStudiesTaskResponse:
        raise NotImplementedError()
