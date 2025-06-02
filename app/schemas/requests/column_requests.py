from pydantic import BaseModel


class CreateColumnRequest(BaseModel):
    title: str
    board_id: int


class DeleteColumnRequest(BaseModel):
    id: int
    board_id: int


class UpdateColumnRequest(BaseModel):
    column_id: int
    title: str
