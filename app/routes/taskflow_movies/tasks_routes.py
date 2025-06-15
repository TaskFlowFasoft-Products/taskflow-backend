from fastapi import APIRouter, Depends, Query, status

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow_movies.tasks import get_movies_tasks_services
from app.interfaces.services.taskflow_movies.tasks_services_interface import IMoviesTasksServices
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.requests.taskflow_movies.tasks_requests import (
    CreateMoviesTaskRequest,
    UpdateMoviesTaskRequest,
    DeleteMoviesTaskRequest
)
from app.schemas.responses.taskflow_movies.tasks_responses import (
    GetMoviesTasksResponse,
    CreateMoviesTaskResponse,
    UpdateMoviesTaskResponse
)

movies_tasks = APIRouter(
    prefix="/movies/tasks",
    tags=["TaskFlow Movies - Tasks"]
)


@movies_tasks.post("", response_model=CreateMoviesTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_movies_task(
    tasks_request: CreateMoviesTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesTasksServices = Depends(get_movies_tasks_services)
) -> CreateMoviesTaskResponse:
    return await movies_services.create_task(tasks_request, user_data)


@movies_tasks.get("", response_model=GetMoviesTasksResponse)
async def get_movies_tasks_in_column(
    board_id: int = Query(title="ID do Quadro", description="ID do quadro ao qual a coluna pertence."),
    column_id: int = Query(title="ID da Coluna", description="ID da coluna cujas tarefas serão listadas."),
    user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesTasksServices = Depends(get_movies_tasks_services)
) -> GetMoviesTasksResponse:
    return await movies_services.get_tasks_in_column(board_id, column_id, user_data)


@movies_tasks.put("", response_model=UpdateMoviesTaskResponse)
async def update_movies_task(
    tasks_request: UpdateMoviesTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesTasksServices = Depends(get_movies_tasks_services)
) -> UpdateMoviesTaskResponse:
    return await movies_services.update_task(tasks_request, user_data)


@movies_tasks.delete("", response_model=DeleteTaskResponse)
async def delete_movies_task(
    tasks_request: DeleteMoviesTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    movies_services: IMoviesTasksServices = Depends(get_movies_tasks_services)
) -> DeleteTaskResponse:
    return await movies_services.delete_task(tasks_request, user_data)
