from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.repository.taskflow.board_repository_interface import IBoardRepository
from app.schemas.board_enum import ProductType
from app.schemas.requests.taskflow.board_requests import BoardUpdateRequest
from app.schemas.responses.taskflow.board_responses import Board


class BoardRepository(IBoardRepository):

    def __init__(self, connection: AsyncSession):
        self.connection = connection

    async def check_board_existency(self, board_id: int, user_id: int) -> bool:
        check_existency = await self.connection.execute(
            statement=text(
                "SELECT * FROM BOARDS WHERE ID = :board_id AND USER_ID = :user_id"
            ),
            params={
                "board_id": board_id,
                "user_id": user_id
            }
        )

        return False if not check_existency.scalar() else True

    async def get_user_boards(self, user_id: int, product_type: ProductType) -> Optional[List[Board]]:
        result = await self.connection.execute(
            statement=text(
                "SELECT * FROM BOARDS WHERE USER_ID = :user_id AND product_type = :product_type"
            ),
            params={"user_id": user_id, "product_type": product_type}
        )

        boards = result.mappings().all()

        if not boards:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Quadros não encontrados para o user_id informado."
            )

        return [Board(**board) for board in boards]

    async def delete_board(self, board_id: int, user_id: int):
        exists = await self.check_board_existency(board_id, user_id)

        if not exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quadro não encontrado."
            )
        try:
            await self.connection.execute(
                statement=text("DELETE FROM BOARDS WHERE ID = :board_id AND USER_ID = :user_id"),
                params={
                    "board_id": board_id,
                    "user_id": user_id
                }
            )

            await self.connection.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao tentar excluir o quadro."
            )

    async def create_board(self, title: str, user_id: int, product_type: ProductType) -> dict:
        result = await self.connection.execute(
            statement=text(
                """
                INSERT INTO BOARDS (
                    TITLE,
                    USER_ID,
                    CREATED_AT,
                    PRODUCT_TYPE
                )
                VALUES (
                    :title,
                    :user_id,
                    CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo',
                    :product_type
                ) RETURNING ID, CREATED_AT
                """
            ),
            params={
                "title": title,
                "user_id": user_id,
                "product_type": product_type.value
            }
        )

        board_info = result.mappings().first()

        if board_info:
            await self.connection.commit()

            return dict(board_info)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao criar o quadro."
            )

    async def update_board(
            self,
            board_request: BoardUpdateRequest,
            board_id: int,
            user_id: int
    ) -> dict:
        exists = await self.check_board_existency(board_id, user_id)

        if not exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quadro não encontrado."
            )

        result = await self.connection.execute(
            statement=text(
                """
                UPDATE
                    BOARDS
                SET TITLE = :title
                WHERE ID = :board_id 
                AND USER_ID = :user_id
                RETURNING TITLE
                """
            ),
            params={
                "title": board_request.title,
                "board_id": board_id,
                "user_id": user_id
            }
        )

        update_info = result.mappings().first()

        if update_info:
            await self.connection.commit()

            return dict(update_info)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ocorreu um erro ao atualizar o quadro."
            )
