from typing import List

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.column_repository_interface import  IColumnRepository
from app.schemas.requests.column_requests import CreateColumnRequest, DeleteColumnRequest, UpdateColumnRequest
from app.schemas.responses.column_responses import Column


class ColumnRepository(IColumnRepository):

    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def create_column(self, column_request: CreateColumnRequest) -> dict:
        result = await self.connection.execute(
            statement=text(
                """
                INSERT INTO BOARD_COLUMNS (
                    TITLE,
                    BOARD_ID,
                    CREATED_AT
                )
                VALUES (
                    :title,
                    :board_id,
                    CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo'
                ) RETURNING ID, CREATED_AT
                """
            ),
            params={
                "title": column_request.title,
                "board_id": column_request.board_id
            }
        )

        column_info = result.mappings().first()

        if column_info:
            await self.connection.commit()

            return dict(column_info)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao tentar criar a coluna."
            )

    async def check_column_existency(self, column_id: int, board_id: int) -> bool:
        check_existency = await self.connection.execute(
            statement=text(
                "SELECT * FROM BOARD_COLUMNS WHERE ID = :column_id AND BOARD_ID = :board_id"
            ),
            params={
                "column_id": column_id,
                "board_id": board_id
            }
        )

        return False if not check_existency.scalar() else True

    async def delete_column(self, column_request: DeleteColumnRequest):
        check_existency = await self.check_column_existency(column_request.id, column_request.board_id)

        if not check_existency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )
        else:
            try:
                await self.connection.execute(
                    statement=text(
                        "DELETE FROM BOARD_COLUMNS WHERE ID = :id AND BOARD_ID = :board_id"
                    ),
                    params={
                        "id": column_request.id,
                        "board_id": column_request.board_id
                    }
                )

                await self.connection.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ocorreu um erro ao deletar o coluna."
                )

    async def get_board_columns(self, board_id: int) -> List[Column]:
        result = await self.connection.execute(
            statement=text(
                "SELECT * FROM BOARD_COLUMNS WHERE BOARD_ID = :board_id"
            ),
            params={"board_id": board_id}
        )

        columns = result.mappings().all()

        if not columns:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Não há colunas cadastradas para o board_id informado."
            )

        return [Column(**column) for column in columns]

    async def update_column(self, board_id: int, column_request: UpdateColumnRequest) -> dict:
        check_existency = await self.check_column_existency(column_request.column_id, board_id)

        if not check_existency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Coluna não encontrada."
            )
        else:
            result = await self.connection.execute(
                statement=text(
                    """
                    UPDATE
                        BOARD_COLUMNS
                    SET TITLE = :title
                    WHERE ID = :id
                    AND BOARD_ID = :board_id
                    RETURNING TITLE
                    """
                ),
                params={
                    "title": column_request.title,
                    "id": column_request.column_id,
                    "board_id": board_id
                }
            )

            update_info = result.mappings().first()

            if update_info:
                await self.connection.commit()

                return dict(update_info)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ocorreu um erro ao atualizar a coluna."
                )
