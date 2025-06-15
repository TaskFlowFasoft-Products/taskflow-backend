from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.authentication_routes import authentication
from app.routes.taskflow.board_routes import base_boards
from app.routes.taskflow.column_routes import base_column
from app.routes.taskflow.tasks_routes import base_tasks
from app.routes.taskflow_studies.board_routes import studies_board
from app.routes.taskflow_studies.tasks_routes import studies_tasks

app = FastAPI(
    title="API TaskFlow",
    description="API responsável pelas requisições do TaskFlow.",
    openapi_url=None,
    redoc_url=None,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    }
)

app.include_router(authentication)
app.include_router(base_boards)
app.include_router(base_column)
app.include_router(base_tasks)
app.include_router(studies_board)
app.include_router(studies_tasks)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
