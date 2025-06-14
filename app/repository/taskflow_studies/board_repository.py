from typing import List, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.taskflow_studies.board_repository_interface import IBoardStudiesRepository


class BoardStudiesRepository(IBoardStudiesRepository):

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
                FROM STUDIES_BOARD_TEMPLATES
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
                FROM STUDIES_BOARD_TEMPLATES
                WHERE ID = :template_id
                """
            ),
            params={"template_id": template_id}
        )

        return result.mappings().one_or_none()

    async def get_column_templates_by_board_template_id(self, template_id: int) -> List[Dict]:
        result = await self.connection.execute(
            statement=text(
                """
                SELECT
                    NAME,
                    COLUMN_ORDER
                FROM STUDIES_COLUMN_TEMPLATES
                WHERE BOARD_TEMPLATE_ID = :template_id
                ORDER BY COLUMN_ORDER
                """
            ),
            params={"template_id": template_id}
        )

        return [dict(row) for row in result.mappings().all()]
