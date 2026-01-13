from typing import List
from pydantic import BaseModel


class UserRolesUpdateDto(BaseModel):
    roles: List[int]
