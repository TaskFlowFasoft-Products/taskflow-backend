from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.requests.taskflow_studies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow_studies.board_responses import GetBoardTemplatesResponse
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse


class IBoardStudiesServices(ABC):

    @abstractmethod
    async def list_board_templates(self) -> GetBoardTemplatesResponse:
        raise NotImplementedError()

    @abstractmethod
    async def add_board_from_template(
        self,
        template: CreateBoardFromTemplateRequest,
        user_data: UserJWTData
    ) -> BoardCreatedResponse:
        raise NotImplementedError()
