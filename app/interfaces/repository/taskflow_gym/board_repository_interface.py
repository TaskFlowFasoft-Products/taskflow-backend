from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class IGymBoardRepository(ABC):

    @abstractmethod
    async def get_board_templates(self) -> List[Dict]:
        raise NotImplementedError()

    @abstractmethod
    async def get_template_details(self, template_id: int) -> Optional[Dict]:
        raise NotImplementedError()

    @abstractmethod
    async def get_column_templates(self) -> List[Dict]:
        raise NotImplementedError()
