from typing import Optional, List
from datetime import date, datetime

from pydantic import BaseModel

class StudiesTaskResponse(BaseModel):
    id: int
    title: str
    description: str
    column_id: int
    created_at: datetime
    due_date: Optional[date] = None
    completion_image_base64: Optional[str] = None


class GetStudiesTasksResponse(BaseModel):
    tasks: List[StudiesTaskResponse]


class CreateStudiesTaskResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    message: str
    due_date: Optional[date] = None


class UpdateStudiesTaskResponse(BaseModel):
    success: bool
    id: int
    message: str
