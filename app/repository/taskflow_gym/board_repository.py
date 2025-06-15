from typing import List, Dict, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.taskflow_gym.board_repository_interface import IGymBoardRepository


class GymBoardRepository(IGymBoardRepository):

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
                FROM GYM_BOARD_TEMPLATES
                ORDER BY ID
                """
            )
        )

        return [dict(row) for row in result.mappings().all()]

    async def get_template_details(self, template_id: int) -> Optional[Dict]:
        result = await self.connection.execute(
            statement=text("SELECT name FROM GYM_BOARD_TEMPLATES WHERE id = :template_id"),
            params={"template_id": template_id}
        )

        return result.mappings().one_or_none()
