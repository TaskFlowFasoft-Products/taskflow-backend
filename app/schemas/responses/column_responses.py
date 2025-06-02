from datetime import datetime
from typing import List

from pydantic import BaseModel


class CreateColumnResponse(BaseModel):
    id: int
    title: str
    board_id: int
    created_at: datetime


class DeleteColumnResponse(BaseModel):
    success: bool
    column_id: int
    message: str


class Column(BaseModel):
    id: int
    title: str
    board_id: int
    created_at: datetime


class GetColumnsResponse(BaseModel):
    columns: List[Column]


class UpdateColumnResponse(BaseModel):
    success: bool
    id: int
    message: str
    fields_updated: List
