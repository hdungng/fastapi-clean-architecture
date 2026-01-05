from pydantic import BaseModel


class TokenResponseDto(BaseModel):
    AccessToken: str
    TokenType: str = "bearer"
    RefreshToken: str | None = None
