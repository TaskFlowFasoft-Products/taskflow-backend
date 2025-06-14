from pydantic import BaseModel


class CreateBoardRequest(BaseModel):
    title: str


class BoardUpdateRequest(BaseModel):
    title: str
