from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.entities.User import User


class IUserRepository(ABC):
    @abstractmethod
    async def GetAll(self) -> List[User]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def GetByUserName(self, user_name: str) -> Optional[User]:
        pass

    @abstractmethod
    async def Search(
        self,
        page: int,
        page_size: int,
        sort_by: str | None,
        sort_dir: str,
        search: str | None,
        is_active: bool | None,
    ) -> Tuple[List[User], int]:
        """Trả về (items, total)"""
        pass

    @abstractmethod
    async def Add(self, entity: User) -> User:
        pass

    @abstractmethod
    async def Update(self, entity: User) -> User:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass
