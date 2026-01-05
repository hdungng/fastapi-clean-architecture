from abc import ABC, abstractmethod
from typing import List

from app.application.dtos.PermissionDto import PermissionDto


class IPermissionService(ABC):
    @abstractmethod
    async def GetAll(self) -> List[PermissionDto]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> PermissionDto | None:
        pass

    @abstractmethod
    async def Create(self, dto: PermissionDto) -> PermissionDto:
        pass

    @abstractmethod
    async def Update(self, id: int, dto: PermissionDto) -> PermissionDto:
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
