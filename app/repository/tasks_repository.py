from typing import List

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.tasks_repository_interface import ITasksRepository
from app.schemas.requests.tasks_requests import CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest


class TasksRepository(ITasksRepository):

    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def create_task(self, tasks_request: CreateTaskRequest) -> dict:
        result = await self.connection.execute(
            statement=text(
                """
                INSERT INTO TASKS(
                    TITLE,
                    DESCRIPTION,
                    COLUMN_ID,
                    DUE_DATE,
                    CREATED_AT
                )
                VALUES (
                    :title,
                    :description,
                    :column_id,
                    :due_date,
                    CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo'
                ) RETURNING ID, CREATED_AT
                """
            ),
            params={
                "title": tasks_request.title,
                "description": tasks_request.description,
                "column_id": tasks_request.column_id,
                "due_date": tasks_request.due_date
            }
        )

        task_info = result.mappings().first()

        if task_info:
            await self.connection.commit()

            return dict(task_info)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao criar a task."
            )

    async def get_column_tasks(self, column_id: int) -> List:
        result = await self.connection.execute(
            statement=text(
                "SELECT * FROM TASKS WHERE COLUMN_ID = :column_id"
            ),
            params={"column_id": column_id}
        )

        tasks = result.mappings().all()

        if tasks:
            return [dict(**task) for task in tasks]
        else:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Ocorreu um erro ao consultar as tasks."
            )

    async def check_task_existency(self, task_id: int, column_id: int) -> bool:
        check_existency = await self.connection.execute(
            statement=text(
                "SELECT * FROM TASKS WHERE ID = :task_id AND COLUMN_ID = :column_id"
            ),
            params={
                "task_id": task_id,
                "column_id": column_id
            }
        )

        return False if not check_existency.scalar() else True

    async def delete_task(self, tasks_request: DeleteTaskRequest):
        check_existency = await self.check_task_existency(tasks_request.task_id, tasks_request.column_id)

        if not check_existency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tarefa não encontrada."
            )
        else:
            try:
                await self.connection.execute(
                    statement=text(
                        "DELETE FROM TASKS WHERE ID = :task_id AND COLUMN_ID = :column_id"
                    ),
                    params={
                        "task_id": tasks_request.task_id,
                        "column_id": tasks_request.column_id
                    }
                )

                await self.connection.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ocorreu um erro ao deletar a tarefa."
                )

    async def update_task(self, tasks_request: UpdateTaskRequest):
        check_existency = await self.check_task_existency(tasks_request.task_id, tasks_request.old_column_id)

        if not check_existency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )
        else:
            try:
                await self.connection.execute(
                    statement=text(
                        """
                        UPDATE
                            TASKS
                        SET TITLE = :title,
                            DESCRIPTION = :description,
                            COLUMN_ID = :column_id,
                            DUE_DATE = :due_date
                        WHERE ID = :task_id
                        """
                    ),
                    params={
                        "title": tasks_request.title,
                        "description": tasks_request.description,
                        "column_id": tasks_request.column_id,
                        "due_date": tasks_request.due_date,
                        "task_id": tasks_request.task_id
                    }
                )

                await self.connection.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ocorreu um erro ao atualizar a tarefa."
                )
