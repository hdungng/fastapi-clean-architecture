from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.Role import Role
from app.application.dtos.RoleDto import RoleDto


class RoleProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(Role, RoleDto)
        mapper.CreateMap(RoleDto, Role)
