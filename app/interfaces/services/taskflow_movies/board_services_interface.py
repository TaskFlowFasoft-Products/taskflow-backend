from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.requests.taskflow_movies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse
from app.schemas.responses.taskflow_movies.board_responses import GetMoviesBoardTemplatesResponse


class IMoviesBoardServices(ABC):

    @abstractmethod
    async def list_board_templates(self) -> GetMoviesBoardTemplatesResponse:
        raise NotImplementedError()

    @abstractmethod
    async def add_board_from_template(
        self, template: CreateBoardFromTemplateRequest, user_data: UserJWTData
    ) -> BoardCreatedResponse:
        raise NotImplementedError()
