from fastapi import APIRouter, Depends

from app.core.jwt_auth import decode_access_token, UserJWTData
from app.dependencies.taskflow_studies.board import get_studies_board_services
from app.interfaces.services.taskflow_studies.board_services_interface import IBoardStudiesServices
from app.schemas.requests.taskflow_studies.board_requests import CreateBoardFromTemplateRequest
from app.schemas.responses.taskflow_studies.board_responses import GetBoardTemplatesResponse
from app.schemas.responses.taskflow.board_responses import BoardCreatedResponse

studies_board = APIRouter(
    prefix="/studies/boards",
    tags=["TaskFlow Studies - Boards"]
)


@studies_board.get("/templates", response_model=GetBoardTemplatesResponse)
async def get_board_templates(
        _user_data: UserJWTData = Depends(decode_access_token),
        studies_services: IBoardStudiesServices = Depends(get_studies_board_services)
) -> GetBoardTemplatesResponse:
    return await studies_services.list_board_templates()


@studies_board.post("", response_model=BoardCreatedResponse)
async def add_board_from_template(
    template: CreateBoardFromTemplateRequest,
    user_data: UserJWTData = Depends(decode_access_token),
    studies_services: IBoardStudiesServices = Depends(get_studies_board_services)
) -> BoardCreatedResponse:
    return await studies_services.add_board_from_template(template, user_data)
