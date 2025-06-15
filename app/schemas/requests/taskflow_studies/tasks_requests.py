from typing import Optional
from datetime import date

from pydantic import BaseModel


class CreateStudiesTaskRequest(BaseModel):
    board_id: int
    column_id: int
    title: str
    description: str
    due_date: Optional[date] = None


class UpdateStudiesTaskRequest(BaseModel):
    board_id: int
    task_id: int
    column_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    completion_image_base64: Optional[str] = None
