from typing import Optional

from pydantic import BaseModel, Field


class CreateMoviesTaskRequest(BaseModel):
    board_id: int
    column_id: int
    title: str
    description: Optional[str] = None
    recommended_by: Optional[str] = None
    category: Optional[str] = None


class UpdateMoviesTaskRequest(BaseModel):
    task_id: int
    board_id: int
    column_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    recommended_by: Optional[str] = None
    category: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5, description="Avaliação de 1 a 5 estrelas")


class DeleteMoviesTaskRequest(BaseModel):
    task_id: int
    board_id: int
