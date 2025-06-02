from abc import ABC, abstractmethod
from typing import List

from app.schemas.requests.tasks_requests import CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest


class ITasksRepository(ABC):

    @abstractmethod
    async def create_task(self, tasks_request: CreateTaskRequest) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def get_column_tasks(self, column_id: int) -> List:
        raise NotImplementedError()

    @abstractmethod
    async def check_task_existency(self, task_id: int, column_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, tasks_request: DeleteTaskRequest):
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, tasks_request: UpdateTaskRequest):
        raise NotImplementedError()
