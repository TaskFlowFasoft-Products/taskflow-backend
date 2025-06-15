from pydantic import BaseModel
from typing import List


class MoviesBoardTemplateResponse(BaseModel):
    id: int
    name: str
    description: str


class GetMoviesBoardTemplatesResponse(BaseModel):
    templates: List[MoviesBoardTemplateResponse]
