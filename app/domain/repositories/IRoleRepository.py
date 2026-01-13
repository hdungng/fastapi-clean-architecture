from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.Role import Role


class IRoleRepository(ABC):
    @abstractmethod
    async def GetAll(self) -> List[Role]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[Role]:
        pass

    @abstractmethod
    async def GetByName(self, name: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def GetByNames(self, names: List[str]) -> List[Role]:
        """Lấy danh sách Role theo list tên (bỏ qua tên không tồn tại)."""
        pass

    @abstractmethod
    async def GetByIds(self, ids: List[int]) -> List[Role]:
        """Lấy danh sách Role theo list id (bỏ qua id không tồn tại)."""
        pass

    @abstractmethod
    async def Add(self, entity: Role) -> Role:
        pass

    @abstractmethod
    async def Update(self, entity: Role) -> Role:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def AssignRoleToUser(self, user_id: int, role_id: int) -> None:
        pass

    @abstractmethod
    async def RemoveRoleFromUser(self, user_id: int, role_id: int) -> None:
        pass

    @abstractmethod
    async def ClearRolesForUser(self, user_id: int) -> None:
        """Xoá toàn bộ role hiện tại của user."""
        pass

    @abstractmethod
    async def GetRolesByUser(self, user_id: int) -> List[Role]:
        pass
