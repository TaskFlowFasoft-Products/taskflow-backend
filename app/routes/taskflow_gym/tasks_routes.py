from fastapi import APIRouter, Depends, Query, status

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow_gym.tasks import get_gym_tasks_services
from app.interfaces.services.taskflow_gym.tasks_services_interface import IGymTasksServices
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.requests.taskflow_gym.tasks_requests import (
    CreateGymTaskRequest,
    UpdateGymTaskRequest,
    DeleteGymTaskRequest
)
from app.schemas.responses.taskflow_gym.tasks_responses import (
    GetGymTasksResponse,
    CreateGymTaskResponse,
    UpdateGymTaskResponse
)

gym_tasks = APIRouter(
    prefix="/gym/tasks",
    tags=["TaskFlow Gym - Tasks"]
)


@gym_tasks.post("", response_model=CreateGymTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_gym_task(
    request: CreateGymTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymTasksServices = Depends(get_gym_tasks_services)
) -> CreateGymTaskResponse:
    return await gym_services.create_task(request, user_data)


@gym_tasks.get("", response_model=GetGymTasksResponse)
async def get_gym_tasks_in_column(
    board_id: int = Query(title="ID do Quadro", description="ID do quadro ao qual a coluna pertence."),
    column_id: int = Query(title="ID da Coluna", description="ID da coluna cujas tarefas serão listadas."),
    user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymTasksServices = Depends(get_gym_tasks_services)
) -> GetGymTasksResponse:
    return await gym_services.get_tasks_in_column(board_id, column_id, user_data)


@gym_tasks.put("", response_model=UpdateGymTaskResponse)
async def update_gym_task(
    request: UpdateGymTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymTasksServices = Depends(get_gym_tasks_services)
) -> UpdateGymTaskResponse:
    return await gym_services.update_task(request, user_data)


@gym_tasks.delete("", response_model=DeleteTaskResponse)
async def delete_gym_task(
    request: DeleteGymTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    gym_services: IGymTasksServices = Depends(get_gym_tasks_services)
) -> DeleteTaskResponse:
    return await gym_services.delete_task(request, user_data)
