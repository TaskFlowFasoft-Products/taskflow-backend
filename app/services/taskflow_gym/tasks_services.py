from datetime import datetime, timedelta

from fastapi import HTTPException, status

from app.core.jwt_auth import UserJWTData
from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.interfaces.repository.taskflow.column_repository_interface import IColumnRepository
from app.interfaces.repository.taskflow.tasks_repository_interface import ITasksRepository
from app.interfaces.services.taskflow_gym.tasks_services_interface import IGymTasksServices
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.requests.taskflow_gym.tasks_requests import (
    CreateGymTaskRequest,
    UpdateGymTaskRequest,
    DeleteGymTaskRequest
)
from app.schemas.responses.taskflow_gym.tasks_responses import (
    GetGymTasksResponse,
    GymTaskResponse,
    CreateGymTaskResponse,
    UpdateGymTaskResponse
)


class GymTasksServices(IGymTasksServices):
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

    async def create_task(self, request: CreateGymTaskRequest, user_data: UserJWTData) -> CreateGymTaskResponse:
        await self._verify_board_and_column_ownership(request.board_id, request.column_id, user_data.user_id)

        warning_message = None

        if request.muscle_group:
            last_training_date = await self.tasks_repository.get_most_recent_task_date_for_muscle_group(
                user_id=user_data.user_id,
                muscle_group=request.muscle_group
            )

            if last_training_date and (datetime.now(last_training_date.tzinfo) - last_training_date) < timedelta(hours=48):
                warning_message = f"Aviso: O grupo muscular '{request.muscle_group}' foi treinado há menos de 48 horas."

        task_info = await self.tasks_repository.create_task(request)

        return CreateGymTaskResponse(
            id=task_info.get("id"),
            title=request.title,
            created_at=task_info.get("created_at"),
            message="Tarefa do Gym criada com sucesso.",
            warning=warning_message
        )

    async def get_tasks_in_column(self, board_id: int, column_id: int, user_data: UserJWTData) -> GetGymTasksResponse:
        await self._verify_board_and_column_ownership(board_id, column_id, user_data.user_id)

        tasks = await self.tasks_repository.get_column_tasks(column_id)

        gym_tasks = [GymTaskResponse(**task) for task in tasks]

        return GetGymTasksResponse(tasks=gym_tasks)

    async def update_task(self, request: UpdateGymTaskRequest, user_data: UserJWTData) -> UpdateGymTaskResponse:
        if not await self.board_repository.check_board_existency(request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        await self.tasks_repository.update_task(request)

        return UpdateGymTaskResponse(
            success=True,
            id=request.task_id,
            message="Tarefa do Gym atualizada com sucesso."
        )

    async def delete_task(self, request: DeleteGymTaskRequest, user_data: UserJWTData) -> DeleteTaskResponse:
        if not await self.board_repository.check_board_existency(request.board_id, user_data.user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quadro não encontrado ou não pertence ao usuário."
            )

        await self.tasks_repository.delete_task_by_id(request.task_id)

        return DeleteTaskResponse(
            success=True,
            task_id=request.task_id,
            message="Tarefa deletada com sucesso."
        )
