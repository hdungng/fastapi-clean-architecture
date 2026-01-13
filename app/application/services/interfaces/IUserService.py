from abc import ABC, abstractmethod
from typing import List, Optional
from app.application.dtos.UserDto import UserDto
from app.application.dtos.UserCreateDto import UserCreateDto
from app.shared.pagination import PagedResult


class IUserService(ABC):
    @abstractmethod
    async def GetAll(self) -> List[UserDto]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[UserDto]:
        pass

    @abstractmethod
    async def GetPaged(
        self,
        page: int,
        page_size: int,
        sort_by: str | None,
        sort_dir: str,
        search: str | None,
        is_active: bool | None,
    ) -> PagedResult[UserDto]:
        pass

    @abstractmethod
    async def Create(self, dto: UserCreateDto) -> UserDto:
        pass

    @abstractmethod
    async def Update(self, id: int, dto: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def ChangePassword(self, user_id: int, current_password: str, new_password: str) -> None:
        pass

    @abstractmethod
    async def GetCurrentUserProfile(self, user_id: int) -> Optional[UserDto]:
        pass

    @abstractmethod
    async def GetCurrentUserRoles(self, user_id: int) -> List[str]:
        pass

    @abstractmethod
    async def GetCurrentUserPermissions(self, user_id: int) -> List[str]:
        pass


    @abstractmethod
    async def UpdateCurrentUserRoles(self, user_id: int, role_names: List[str]) -> UserDto:
        pass

    @abstractmethod
    async def ChangePassword(self, user_id: int, current_password: str, new_password: str) -> None:
        pass

