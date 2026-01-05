from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.User import User
from app.application.dtos.UserDto import UserDto


class UserProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(User, UserDto)
        mapper.CreateMap(UserDto, User)
