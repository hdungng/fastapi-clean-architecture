from pydantic import BaseModel


class ChangePasswordDto(BaseModel):
    CurrentPassword: str
    NewPassword: str
