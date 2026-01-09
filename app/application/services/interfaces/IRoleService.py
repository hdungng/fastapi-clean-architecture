from abc import ABC, abstractmethod
from typing import List

from app.application.dtos.RoleDto import RoleDto


class IRoleService(ABC):
    @abstractmethod
    async def GetAll(self) -> List[RoleDto]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> RoleDto | None:
        pass

    @abstractmethod
    async def Create(self, dto: RoleDto) -> RoleDto:
        pass

    @abstractmethod
    async def Update(self, id: int, dto: RoleDto) -> RoleDto:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def AssignRoleToUser(self, role_id: int, user_id: int) -> None:
        pass

    @abstractmethod
    async def RemoveRoleFromUser(self, role_id: int, user_id: int) -> None:
        pass
