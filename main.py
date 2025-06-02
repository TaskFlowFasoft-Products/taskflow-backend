from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.authentication_routes import authentication
from app.routes.board_routes import boards
from app.routes.column_routes import column
from app.routes.tasks_routes import tasks

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
app.include_router(boards)
app.include_router(column)
app.include_router(tasks)

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
