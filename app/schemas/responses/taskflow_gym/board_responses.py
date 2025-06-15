from typing import List

from pydantic import BaseModel


class GymBoardTemplateResponse(BaseModel):
    id: int
    name: str
    description: str


class GetGymBoardTemplatesResponse(BaseModel):
    templates: List[GymBoardTemplateResponse]
