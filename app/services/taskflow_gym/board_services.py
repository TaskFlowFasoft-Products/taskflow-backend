from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
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
            board_repository: IBoardRepository,
            column_repository: IColumnRepository
    ):
        self.gym_board_repository = gym_board_repository
        self.board_repository = board_repository
        self.column_repository = column_repository

    async def list_board_templates(self) -> GetGymBoardTemplatesResponse:
        templates = await self.gym_board_repository.get_board_templates()

        return GetGymBoardTemplatesResponse(templates=[GymBoardTemplateResponse(**t) for t in templates])

    async def add_board_from_template(
            self, template: CreateBoardFromTemplateRequest, user_data: UserJWTData
    ) -> BoardCreatedResponse:
        template_details = await self.gym_board_repository.get_template_details(template.id)

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

        board_id = board_info.get("id")

        column_templates = await self.gym_board_repository.get_column_templates()

        if column_templates:
            await self.column_repository.create_columns_in_batch(board_id, column_templates)

        return BoardCreatedResponse(
            board_id=board_id,
            message=f"Quadro '{template_name}' adicionado com sucesso.",
            created_at=board_info.get("created_at")
        )
