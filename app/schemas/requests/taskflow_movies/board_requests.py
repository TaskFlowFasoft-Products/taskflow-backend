from pydantic import BaseModel


class CreateBoardFromTemplateRequest(BaseModel):
    id: int
