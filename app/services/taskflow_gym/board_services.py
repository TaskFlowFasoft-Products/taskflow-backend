from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow_gym.board_repository_interface import IGymBoardRepository
from app.interfaces.services.taskflow_gym.board_services_interface import IGymBoardServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow_gym.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse
from app.schemas.responses.taskflow_gym.board_responses import GetGymBoardTemplatesResponse, GymBoardTemplateResponse


class GymBoardServices(IGymBoardServices):
    def __init__(
            self,
            gym_board_repository: IGymBoardRepository,
            board_repository: IBoardRepository
    ):
        self.gym_board_repository = gym_board_repository
        self.board_repository = board_repository

    async def list_board_templates(self) -> GetGymBoardTemplatesResponse:
        templates = await self.gym_board_repository.get_board_templates()

        return GetGymBoardTemplatesResponse(templates=[GymBoardTemplateResponse(**template) for template in templates])

    async def add_board_from_template(
            self,
            request: CreateBoardFromTemplateRequest,
            user_data: UserJWTData
    ) -> BoardCreatedResponse:
        template_details = await self.gym_board_repository.get_template_details(request.id)

        if not template_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O modelo de quadro solicitado não existe."
            )

        template_name = template_details.get("name")

        board_info = await self.board_repository.create_board(
            title=template_name,
            user_id=user_data.user_id,
            product_type=ProductType.GYM
        )

        return BoardCreatedResponse(
            board_id=board_info.get("id"),
            message=f"Quadro '{template_name}' adicionado com sucesso. Agora, adicione suas colunas (dias de treino).",
            created_at=board_info.get("created_at")
        )
