from pydantic import BaseModel
from typing import List, Optional


class BoardTemplateResponse(BaseModel):
    id: int
    name: str
    description: str


class GetBoardTemplatesResponse(BaseModel):
    templates: Optional[List[BoardTemplateResponse]]
