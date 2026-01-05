from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.Permission import Permission
from app.application.dtos.PermissionDto import PermissionDto


class PermissionProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(Permission, PermissionDto)
        mapper.CreateMap(PermissionDto, Permission)
