from abc import ABC, abstractmethod
from app.application.dtos.LoginRequestDto import LoginRequestDto
from app.application.dtos.TokenResponseDto import TokenResponseDto


class IAuthService(ABC):
    @abstractmethod
    async def Login(self, request: LoginRequestDto) -> TokenResponseDto:
        pass

    @abstractmethod
    async def Refresh(self, refresh_token: str) -> TokenResponseDto:
        pass

    @abstractmethod
    async def RevokeRefreshToken(self, refresh_token: str) -> None:
        pass
