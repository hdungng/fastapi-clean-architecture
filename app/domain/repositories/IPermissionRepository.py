from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.Permission import Permission


class IPermissionRepository(ABC):
    @abstractmethod
    async def GetAll(self) -> List[Permission]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[Permission]:
        pass

    @abstractmethod
    async def GetByName(self, name: str) -> Optional[Permission]:
        pass

    @abstractmethod
    async def Add(self, entity: Permission) -> Permission:
        pass

    @abstractmethod
    async def Update(self, entity: Permission) -> Permission:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def AssignPermissionToRole(self, permission_id: int, role_id: int) -> None:
        pass

    @abstractmethod
    async def RemovePermissionFromRole(self, permission_id: int, role_id: int) -> None:
        pass

    @abstractmethod
    async def GetPermissionsByRole(self, role_id: int) -> List[Permission]:
        pass
