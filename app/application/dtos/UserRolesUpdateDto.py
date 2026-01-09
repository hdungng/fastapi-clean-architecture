from typing import List
from pydantic import BaseModel


class UserRolesUpdateDto(BaseModel):
    Roles: List[str]
