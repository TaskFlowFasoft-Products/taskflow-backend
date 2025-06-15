from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow.tasks_repository_interface import ITasksRepository
from app.interfaces.services.taskflow_movies.tasks_services_interface import IMoviesTasksServices
from app.schemas.requests.taskflow_movies.tasks_requests import CreateMoviesTaskRequest, UpdateMoviesTaskRequest, DeleteMoviesTaskRequest
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.responses.taskflow_movies.tasks_responses import (
    GetMoviesTasksResponse,
    MoviesTaskResponse,
    CreateMoviesTaskResponse,
    UpdateMoviesTaskResponse
)


class MoviesTasksServices(IMoviesTasksServices):

    def __init__(
        self,
        tasks_repository: ITasksRepository,
        board_repository: IBoardRepository,
        column_repository: IColumnRepository
    ):
        self.tasks_repository = tasks_repository
        self.board_repository = board_repository
        self.column_repository = column_repository

    async def _verify_board_and_column_ownership(self, board_id: int, column_id: int, user_id: int):
        if not await self.board_repository.check_board_existency(board_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        if not await self.column_repository.check_column_existency(column_id, board_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Coluna não encontrada neste quadro."
            )

    async def create_task(self, request: CreateMoviesTaskRequest, user_data: UserJWTData) -> CreateMoviesTaskResponse:
        await self._verify_board_and_column_ownership(request.board_id, request.column_id, user_data.user_id)

        task_info = await self.tasks_repository.create_task(request)

        return CreateMoviesTaskResponse(
            id=task_info.get("id"),
            title=request.title,
            description=request.description,
            created_at=task_info.get("created_at"),
            message="Tarefa do movies criada com sucesso.",
            recommended_by=request.recommended_by,
            category=request.category
        )

    async def get_tasks_in_column(self, board_id: int, column_id: int, user_data: UserJWTData) -> GetMoviesTasksResponse:
        await self._verify_board_and_column_ownership(board_id, column_id, user_data.user_id)

        tasks = await self.tasks_repository.get_column_tasks(column_id)

        return GetMoviesTasksResponse(tasks=[MoviesTaskResponse(**task) for task in tasks])

    async def update_task(self, request: UpdateMoviesTaskRequest, user_data: UserJWTData) -> UpdateMoviesTaskResponse:
        if not await self.board_repository.check_board_existency(request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        await self.tasks_repository.update_task(request)

        return UpdateMoviesTaskResponse(
            success=True,
            id=request.task_id,
            message="Tarefa do movies atualizada com sucesso."
        )

    async def delete_task(self, request: DeleteMoviesTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        if not await self.board_repository.check_board_existency(request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        await self.tasks_repository.delete_task_by_id(request.task_id)

        return DeleteTaskResponse(success=True, task_id=request.task_id, message="Tarefa deletada com sucesso.")
