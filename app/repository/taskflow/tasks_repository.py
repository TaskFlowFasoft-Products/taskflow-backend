from typing import Dict

from fastapi import HTTPException, status
from sqlalchemy import text, RowMapping, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.taskflow.tasks_repository_interface import ITasksRepository
from app.schemas.requests.taskflow.tasks_requests import DeleteTaskRequest


class TasksRepository(ITasksRepository):

    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def create_task(self, tasks_request) -> Dict:
        columns = ["TITLE", "DESCRIPTION", "COLUMN_ID", "DUE_DATE", "CREATED_AT"]

        values = [
            ":title",
            ":description",
            ":column_id",
            ":due_date",
            "CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo'"
        ]

        params = {
            "title": tasks_request.title,
            "description": tasks_request.description,
            "column_id": tasks_request.column_id,
            "due_date": getattr(tasks_request, 'due_date', None)
        }

        optional_fields = {
            'completion_image_base64': 'completion_image_base64',  # Studies
            'recommended_by': 'recommended_by',  # Gym
            'rating': 'rating',  # Gym
            'category': 'category'  # Gym
        }

        for attr, column in optional_fields.items():
            if hasattr(tasks_request, attr) and getattr(tasks_request, attr) is not None:
                columns.append(column)
                values.append(f":{attr}")
                params[attr] = getattr(tasks_request, attr)

        sql_query = f"""
            INSERT INTO TASKS(
                {', '.join(columns)}
            )
            VALUES (
                {', '.join(values)}
            ) RETURNING ID, CREATED_AT
        """

        result = await self.connection.execute(statement=text(sql_query), params=params)

        task_info = result.mappings().first()

        if task_info:
            await self.connection.commit()
            return dict(task_info)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ocorreu um erro ao criar a tarefa."
        )

    async def get_column_tasks(self, column_id: int) -> Sequence[RowMapping]:
        result = await self.connection.execute(
            statement=text("SELECT * FROM TASKS WHERE COLUMN_ID = :column_id"),
            params={"column_id": column_id}
        )

        return result.mappings().all()

    async def check_task_existency(self, task_id: int, column_id: int) -> bool:
        result = await self.connection.execute(
            statement=text("SELECT 1 FROM TASKS WHERE ID = :task_id AND COLUMN_ID = :column_id"),
            params={"task_id": task_id, "column_id": column_id}
        )

        return result.scalar_one_or_none() is not None

    async def update_task(self, tasks_request):
        if not await self.check_task_existency_by_id(tasks_request.task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada."
            )

        update_fields = []
        params = {"task_id": tasks_request.task_id}

        field_map = {
            'title': 'TITLE',
            'description': 'DESCRIPTION',
            'column_id': 'COLUMN_ID',
            'due_date': 'DUE_DATE',
            'completion_image_base64': 'COMPLETION_IMAGE_BASE64',
            'recommended_by': 'RECOMMENDED_BY',
            'rating': 'RATING',
            'category': 'CATEGORY'
        }

        for field, column in field_map.items():
            if hasattr(tasks_request, field) and getattr(tasks_request, field) is not None:
                update_fields.append(f"{column} = :{field}")
                params[field] = getattr(tasks_request, field)

        if not update_fields:
            return

        set_clause = ", ".join(update_fields)

        sql_query = f"UPDATE TASKS SET {set_clause} WHERE ID = :task_id"

        await self.connection.execute(statement=text(sql_query), params=params)

        await self.connection.commit()

    async def delete_task(self, tasks_request: DeleteTaskRequest):
        if not await self.check_task_existency(tasks_request.task_id, tasks_request.column_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada."
            )

        await self.delete_task_by_id(tasks_request.task_id)

    async def check_task_existency_by_id(self, task_id: int) -> bool:
        result = await self.connection.execute(
            statement=text("SELECT 1 FROM TASKS WHERE ID = :task_id"),
            params={"task_id": task_id}
        )
        return result.scalar_one_or_none() is not None

    async def delete_task_by_id(self, task_id: int):
        if not await self.check_task_existency_by_id(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada."
            )

        await self.connection.execute(
            statement=text("DELETE FROM TASKS WHERE ID = :task_id"),
            params={"task_id": task_id}
        )

        await self.connection.commit()
