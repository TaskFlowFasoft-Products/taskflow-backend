from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow_movies.board_repository_interface import IMoviesBoardRepository
from app.interfaces.services.taskflow_movies.board_services_interface import IMoviesBoardServices
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow_movies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse
from app.schemas.responses.taskflow_movies.board_responses import (
    GetMoviesBoardTemplatesResponse,
    MoviesBoardTemplateResponse
)


class MoviesBoardServices(IMoviesBoardServices):
    def __init__(
            self,
            movies_board_repository: IMoviesBoardRepository,
            board_repository: IBoardRepository,
            column_repository: IColumnRepository
    ):
        self.movies_board_repository = movies_board_repository
        self.board_repository = board_repository
        self.column_repository = column_repository

    async def list_board_templates(self) -> GetMoviesBoardTemplatesResponse:
        templates = await self.movies_board_repository.get_board_templates()

        return GetMoviesBoardTemplatesResponse(templates=[MoviesBoardTemplateResponse(**t) for t in templates])

    async def add_board_from_template(
            self, template: CreateBoardFromTemplateRequest, user_data: UserJWTData
    ) -> BoardCreatedResponse:
        template_details = await self.movies_board_repository.get_template_details(template.id)

        if not template_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O modelo de quadro solicitado não existe."
            )

        template_name = template_details.get("name")

        board_info = await self.board_repository.create_board(
            title=template_name,
            user_id=user_data.user_id,
            product_type=ProductType.MOVIES
        )

        board_id = board_info.get("id")

        column_templates = await self.movies_board_repository.get_column_templates()

        if column_templates:
            await self.column_repository.create_columns_in_batch(board_id, column_templates)

        return BoardCreatedResponse(
            board_id=board_id,
            message=f"Quadro '{template_name}' adicionado com sucesso.",
            created_at=board_info.get("created_at")
        )
