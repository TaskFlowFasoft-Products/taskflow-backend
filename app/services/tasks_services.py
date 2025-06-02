from fastapi import status, HTTPException

from app.interfaces.repository.board_repository_interface import IBoardRepository
from app.interfaces.repository.column_repository_interface import IColumnRepository
from app.interfaces.repository.tasks_repository_interface import ITasksRepository
from app.interfaces.services.tasks_services_interface import ITasksServices
from app.schemas.requests.authentication_requests import UserJWTData
from app.schemas.requests.tasks_requests import CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest
from app.schemas.responses.tasks_responses import (
    CreateTaskResponse,
    GetColumnTasksResponse,
    DeleteTaskResponse,
    UpdateTaskResponse
)


class TasksServices(ITasksServices):

    def __init__(
            self,
            column_repository: IColumnRepository,
            board_repository: IBoardRepository,
            tasks_repository: ITasksRepository
    ):
        self.column_repository = column_repository
        self.board_repository = board_repository
        self.tasks_repository = tasks_repository

    async def create_task(self, tasks_request: CreateTaskRequest, user_data: UserJWTData) -> CreateTaskResponse:
        board_exists = await self.board_repository.check_board_existency(tasks_request.board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        column_exists = await self.column_repository.check_column_existency(
            tasks_request.column_id,
            tasks_request.board_id
        )

        if not column_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )

        task = await self.tasks_repository.create_task(tasks_request)

        return CreateTaskResponse(
            id=task.get("id"),
            title=tasks_request.title,
            description=tasks_request.description,
            due_date=tasks_request.due_date,
            created_at=task.get("created_at"),
            message="Tarefa criada com sucesso."
        )

    async def get_column_tasks(self, column_id: int, board_id: int, user_data: UserJWTData) -> GetColumnTasksResponse:
        board_exists = await self.board_repository.check_board_existency(board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        column_exists = await self.column_repository.check_column_existency(column_id, board_id)

        if not column_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )

        tasks = await self.tasks_repository.get_column_tasks(column_id)

        return GetColumnTasksResponse(tasks=tasks)

    async def delete_task(self, tasks_request: DeleteTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        board_exists = await self.board_repository.check_board_existency(tasks_request.board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        column_exists = await self.column_repository.check_column_existency(
            tasks_request.column_id,
            tasks_request.board_id
        )

        if not column_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )

        await self.tasks_repository.delete_task(tasks_request)

        return DeleteTaskResponse(
            success=True,
            task_id=tasks_request.task_id,
            message="Tarefa deletada com sucesso."
        )

    async def update_task(self, tasks_request: UpdateTaskRequest, user_data: UserJWTData) -> UpdateTaskResponse:
        board_exists = await self.board_repository.check_board_existency(tasks_request.board_id, user_data.user_id)

        if not board_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quadro informado não encontrado."
            )

        column_exists = await self.column_repository.check_column_existency(
            tasks_request.column_id,
            tasks_request.board_id
        )

        if not column_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )

        await self.tasks_repository.update_task(tasks_request)

        return UpdateTaskResponse(
            success=True,
            id=tasks_request.task_id,
            message="Tarefa atualizada com sucesso."
        )
