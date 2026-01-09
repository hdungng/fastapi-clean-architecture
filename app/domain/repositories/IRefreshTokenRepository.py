from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.RefreshToken import RefreshToken


class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def Add(self, entity: RefreshToken) -> RefreshToken:
        pass

    @abstractmethod
    async def GetByToken(self, token: str) -> Optional[RefreshToken]:
        pass

    @abstractmethod
    async def Revoke(self, token: RefreshToken) -> None:
        pass

    @abstractmethod
    async def RevokeAllForUser(self, user_id: int) -> None:
        pass

    @abstractmethod
    async def GetValidTokensForUser(self, user_id: int) -> List[RefreshToken]:
        pass
