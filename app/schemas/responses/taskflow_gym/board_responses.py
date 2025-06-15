from pydantic import BaseModel
from typing import List


class GymBoardTemplateResponse(BaseModel):
    id: int
    name: str
    description: str


class GetGymBoardTemplatesResponse(BaseModel):
    templates: List[GymBoardTemplateResponse]
