from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: str
    column_id: int
    due_date: Optional[date] = None
    created_at: datetime


class CreateTaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: Optional[date] = None
    created_at: datetime
    message: str


class GetColumnTasksResponse(BaseModel):
    tasks: List[Task]


class DeleteTaskResponse(BaseModel):
    success: bool
    task_id: int
    message: str


class UpdateTaskResponse(BaseModel):
    success: bool
    id: int
    message: str
