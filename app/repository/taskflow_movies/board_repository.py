from typing import List, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.taskflow_movies.board_repository_interface import IMoviesBoardRepository


class MoviesBoardRepository(IMoviesBoardRepository):

    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def get_board_templates(self) -> List[Dict]:
        result = await self.connection.execute(
            statement=text(
                """
                SELECT
                    ID,
                    NAME,
                    DESCRIPTION
                FROM MOVIES_BOARD_TEMPLATES
                ORDER BY ID
                """
            )
        )

        return [dict(row) for row in result.mappings().all()]

    async def get_template_details(self, template_id: int) -> Optional[Dict]:
        result = await self.connection.execute(
            statement=text(
                """
                SELECT
                    NAME
                FROM MOVIES_BOARD_TEMPLATES
                WHERE ID = :template_id
                """
            ),
            params={"template_id": template_id}
        )

        return result.mappings().one_or_none()

    async def get_column_templates(self) -> List[Dict]:
        result = await self.connection.execute(
            statement=text(
                """
                SELECT
                    NAME
                FROM MOVIES_COLUMN_TEMPLATES
                ORDER BY COLUMN_ORDER
                """
            )
        )

        return [dict(row) for row in result.mappings().all()]
