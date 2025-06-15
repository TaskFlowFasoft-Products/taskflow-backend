from abc import ABC, abstractmethod
from typing import Sequence, Dict, Optional
from datetime import datetime

from sqlalchemy import RowMapping

from app.schemas.requests.taskflow.tasks_requests import DeleteTaskRequest

class ITasksRepository(ABC):

    @abstractmethod
    async def create_task(self, tasks_request) -> Dict:
        raise NotImplementedError()

    @abstractmethod
    async def get_column_tasks(self, column_id: int) -> Sequence[RowMapping]:
        raise NotImplementedError()

    @abstractmethod
    async def check_task_existency(self, task_id: int, column_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def update_task(self, tasks_request):
        raise NotImplementedError()

    @abstractmethod
    async def delete_task(self, tasks_request: DeleteTaskRequest):
        raise NotImplementedError()

    @abstractmethod
    async def check_task_existency_by_id(self, task_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_task_by_id(self, task_id: int):
        raise NotImplementedError()

    @abstractmethod
    async def get_most_recent_task_date_for_muscle_group(self, user_id: int, muscle_group: str) -> Optional[datetime]:
        raise NotImplementedError()
