from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class GymTaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    column_id: int
    created_at: datetime
    recommended_by: Optional[str] = None
    rating: Optional[int] = None
    category: Optional[str] = None


class GetGymTasksResponse(BaseModel):
    tasks: List[GymTaskResponse]


class CreateGymTaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_at: datetime
    message: str
    recommended_by: Optional[str] = None
    category: Optional[str] = None


class UpdateGymTaskResponse(BaseModel):
    success: bool
    id: int
    message: str
