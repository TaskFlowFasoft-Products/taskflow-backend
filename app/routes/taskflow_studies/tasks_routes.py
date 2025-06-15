from fastapi import APIRouter, Depends, Query, status

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow_studies.tasks import get_studies_tasks_services
from app.interfaces.services.taskflow_studies.tasks_services_interface import IStudiesTasksServices
from app.schemas.requests.taskflow.tasks_requests import DeleteTaskRequest
from app.schemas.requests.taskflow_studies.tasks_requests import CreateStudiesTaskRequest, UpdateStudiesTaskRequest
from app.schemas.responses.taskflow.tasks_responses import DeleteTaskResponse
from app.schemas.responses.taskflow_studies.tasks_responses import (
    GetStudiesTasksResponse,
    CreateStudiesTaskResponse,
    UpdateStudiesTaskResponse
)

studies_tasks = APIRouter(
    prefix="/studies/tasks",
    tags=["TaskFlow Studies - Tasks"]
)


@studies_tasks.post("", response_model=CreateStudiesTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_studies_task(
    tasks_request: CreateStudiesTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    studies_services: IStudiesTasksServices = Depends(get_studies_tasks_services)
) -> CreateStudiesTaskResponse:
    return await studies_services.create_task(tasks_request, user_data)


@studies_tasks.get("", response_model=GetStudiesTasksResponse)
async def get_tasks_in_column(
    column_id: int = Query(title="ID da Coluna"),
    board_id: int = Query(title="ID do Quadro ao qual a coluna pertence"),
    user_data: UserJWTData = Depends(decode_access_token),
    studies_services: IStudiesTasksServices = Depends(get_studies_tasks_services)
) -> GetStudiesTasksResponse:
    return await studies_services.get_tasks_in_column(board_id, column_id, user_data)


@studies_tasks.delete("", response_model=DeleteTaskResponse)
async def delete_studies_task(
        tasks_request: DeleteTaskRequest,
        user_data: UserJWTData = Depends(decode_access_token),
        studies_services: IStudiesTasksServices = Depends(get_studies_tasks_services)
) -> DeleteTaskResponse:
    return await studies_services.delete_task(tasks_request, user_data)


@studies_tasks.put("", response_model=UpdateStudiesTaskResponse)
async def update_studies_task(
    tasks_request: UpdateStudiesTaskRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    studies_services: IStudiesTasksServices = Depends(get_studies_tasks_services)
) -> UpdateStudiesTaskResponse:
    return await studies_services.update_task(tasks_request, user_data)
