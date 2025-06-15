from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow.tasks_repository_interface import ITasksRepository
from app.interfaces.services.taskflow_studies.tasks_services_interface import IStudiesTasksServices
from app.schemas.requests.taskflow.tasks_requests import DeleteTaskRequest
from app.schemas.requests.taskflow_studies.tasks_requests import CreateStudiesTaskRequest, UpdateStudiesTaskRequest
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.responses.taskflow_studies.tasks_responses import (
    GetStudiesTasksResponse,
    StudiesTaskResponse,
    CreateStudiesTaskResponse,
    UpdateStudiesTaskResponse
)


class StudiesTasksServices(IStudiesTasksServices):

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

    async def create_task(
            self,
            tasks_request: CreateStudiesTaskRequest,
            user_data: UserJWTData
    ) -> CreateStudiesTaskResponse:
        await self._verify_board_and_column_ownership(
            tasks_request.board_id,
            tasks_request.column_id,
            user_data.user_id)

        task_info = await self.tasks_repository.create_task(tasks_request)

        return CreateStudiesTaskResponse(
            id=task_info.get("id"),
            title=tasks_request.title,
            description=tasks_request.description,
            due_date=tasks_request.due_date,
            created_at=task_info.get("created_at"),
            message="Tarefa de estudos criada com sucesso."
        )

    async def get_tasks_in_column(
            self,
            board_id: int,
            column_id: int,
            user_data: UserJWTData
    ) -> GetStudiesTasksResponse:
        await self._verify_board_and_column_ownership(board_id, column_id, user_data.user_id)

        tasks = await self.tasks_repository.get_column_tasks(column_id)

        studies_tasks = [StudiesTaskResponse(**task) for task in tasks]

        return GetStudiesTasksResponse(tasks=studies_tasks)

    async def update_task(
            self,
            tasks_request: UpdateStudiesTaskRequest,
            user_data: UserJWTData
    ) -> UpdateStudiesTaskResponse:
        if not await self.board_repository.check_board_existency(tasks_request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        await self.tasks_repository.update_task(tasks_request)

        return UpdateStudiesTaskResponse(
            success=True,
            id=tasks_request.task_id,
            message="Tarefa de estudos atualizada com sucesso."
        )

    async def delete_task(self, tasks_request: DeleteTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        if not await self.board_repository.check_board_existency(tasks_request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado."
            )

        if not await self.column_repository.check_column_existency(
            tasks_request.column_id,
            tasks_request.board_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )

        await self.tasks_repository.delete_task_by_id(tasks_request.task_id)

        return DeleteTaskResponse(success=True, task_id=tasks_request.task_id, message="Tarefa deletada com sucesso.")
