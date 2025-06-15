from abc import ABC, abstractmethod

from app.core.jwt_auth import UserJWTData
from app.schemas.requests.taskflow_gym.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse
from app.schemas.responses.taskflow_gym.board_responses import GetGymBoardTemplatesResponse


class IGymBoardServices(ABC):

    @abstractmethod
    async def list_board_templates(self) -> GetGymBoardTemplatesResponse:
        raise NotImplementedError()

    @abstractmethod
    async def add_board_from_template(
        self, template: CreateBoardFromTemplateRequest, user_data: UserJWTData
    ) -> BoardCreatedResponse:
        raise NotImplementedError()
