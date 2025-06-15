from typing import Optional

from pydantic import BaseModel, Field


class CreateGymTaskRequest(BaseModel):
    board_id: int
    column_id: int
    title: str
    sets_reps: Optional[str] = Field(None, description="Ex: '3x12', '4x10'")
    distance_time: Optional[str] = Field(None, description="Ex: '5 km / 25 min'")
    pace_speed: Optional[str] = Field(None, description="Ex: '5:00/km', '12 km/h'")
    run_screenshot_base64: Optional[str] = None
    rpe_scale: Optional[int] = Field(None, ge=1, le=10, description="Escala de percepção de esforço de 1 a 10")
    muscle_group: Optional[str] = Field(None, description="Ex: 'Peito', 'Pernas'")


class UpdateGymTaskRequest(BaseModel):
    task_id: int
    board_id: int
    column_id: Optional[int] = None
    title: Optional[str] = None
    sets_reps: Optional[str] = None
    distance_time: Optional[str] = None
    pace_speed: Optional[str] = None
    run_screenshot_base64: Optional[str] = None
    rpe_scale: Optional[int] = Field(None, ge=1, le=10)
    muscle_group: Optional[str] = None


class DeleteGymTaskRequest(BaseModel):
    task_id: int
    board_id: int
