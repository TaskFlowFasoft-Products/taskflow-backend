from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow_studies.board_repository_interface import IBoardStudiesRepository
from app.interfaces.services.taskflow_studies.board_services_interface import IBoardStudiesServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow_studies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow_studies.board_responses import GetBoardTemplatesResponse, BoardTemplateResponse
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse


class BoardStudiesServices(IBoardStudiesServices):

    def __init__(
        self,
        studies_repository: IBoardStudiesRepository,
        board_repository: IBoardRepository,
        column_repository: IColumnRepository
    ):
        self.studies_repository = studies_repository
        self.board_repository = board_repository
        self.column_repository = column_repository

    async def list_board_templates(self) -> GetBoardTemplatesResponse:
        templates = await self.studies_repository.get_board_templates()

        return GetBoardTemplatesResponse(
            templates=[BoardTemplateResponse(**template) for template in templates] if templates else None
        )

    async def add_board_from_template(
        self,
        template: CreateBoardFromTemplateRequest,
        user_data: UserJWTData
    ) -> BoardCreatedResponse:
        template_details = await self.studies_repository.get_template_details(template.id)

        if not template_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O modelo de quadro solicitado não existe."
            )

        template_name = template_details.get("name")

        board_info = await self.board_repository.create_board(
            title=template_name,
            user_id=user_data.user_id,
            product_type=ProductType.STUDIES
        )

        board_id = board_info.get("id")

        column_templates = await self.studies_repository.get_column_templates_by_board_template_id(template.id)

        if column_templates:
            await self.column_repository.create_columns_in_batch(board_id, column_templates)

        return BoardCreatedResponse(
            board_id=board_id,
            message=f"Quadro '{template_name}' adicionado com sucesso.",
            created_at=board_info.get("created_at")
        )
