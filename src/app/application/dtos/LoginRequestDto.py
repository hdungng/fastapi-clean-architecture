from pydantic import BaseModel


class LoginRequestDto(BaseModel):
    UserName: str
    Password: str
