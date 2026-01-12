from pydantic import BaseModel


class LoginRequestDto(BaseModel):
    user_name: str
    password: str
