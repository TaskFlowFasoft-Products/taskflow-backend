from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class GymTaskResponse(BaseModel):
    id: int
    title: str
    column_id: int
    created_at: datetime
    sets_reps: Optional[str] = None
    distance_time: Optional[str] = None
    pace_speed: Optional[str] = None
    run_screenshot_base64: Optional[str] = None
    rpe_scale: Optional[int] = None
    muscle_group: Optional[str] = None


class GetGymTasksResponse(BaseModel):
    tasks: List[GymTaskResponse]


class CreateGymTaskResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    message: str
    warning: Optional[str] = None


class UpdateGymTaskResponse(BaseModel):
    success: bool
    id: int
    message: str
