from abc import ABC, abstractmethod
from typing import List, Optional
from app.application.dtos.UserDto import UserDto
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
    async def Create(self, dto: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def Update(self, id: int, dto: UserDto) -> UserDto:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def ChangePassword(self, user_id: int, current_password: str, new_password: str) -> None:
        """Đổi password cho user với kiểm tra current password."""
        pass
