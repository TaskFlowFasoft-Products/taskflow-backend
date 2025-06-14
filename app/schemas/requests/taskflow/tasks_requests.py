from datetime import date
from typing import Optional

from pydantic import BaseModel


class CreateTaskRequest(BaseModel):
    board_id: int
    column_id: int
    title: str
    description: str
    due_date: Optional[date] = None


class DeleteTaskRequest(BaseModel):
    board_id: int
    column_id: int
    task_id: int


class UpdateTaskRequest(BaseModel):
    board_id: int
    task_id: int
    column_id: Optional[int] = None
    old_column_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
