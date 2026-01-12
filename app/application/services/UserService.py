from typing import List, Optional
from app.application.services.interfaces.IUserService import IUserService
from app.application.dtos.UserDto import UserDto
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.domain.entities.User import User
from app.infrastructure.mapping.AutoMapper import MapperInstance
from app.shared.pagination import PagedResult


class UserService(IUserService):
    """
    UserService

    Convention:
    - Xử lý business logic liên quan đến User.
    - Không thao tác trực tiếp với FastAPI Response, chỉ DTO & entity.
    - Tách biệt rõ giữa layer Application và API.
    """

    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def GetAll(self) -> List[UserDto]:
        """Lấy tất cả user (ít dùng, chủ yếu dùng GetPaged)."""
        entities = await self._unit_of_work.Users.GetAll()
        return [MapperInstance.Map(e, UserDto) for e in entities]

    async def GetById(self, id: int) -> Optional[UserDto]:
        """Lấy user theo Id, trả về None nếu không có."""
        entity = await self._unit_of_work.Users.GetById(id)
        return MapperInstance.Map(entity, UserDto) if entity else None

    async def GetPaged(
        self,
        page: int,
        page_size: int,
        sort_by: str | None,
        sort_dir: str,
        search: str | None,
        is_active: bool | None,
    ) -> PagedResult[UserDto]:
        """
        Lấy danh sách user có phân trang + lọc + sắp xếp.

        Trả về:
        - PagedResult[UserDto] với Items, Total, Page, PageSize, TotalPages.
        """
        items, total = await self._unit_of_work.Users.Search(
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir,
            search=search,
            is_active=is_active,
        )
        dto_items = [MapperInstance.Map(e, UserDto) for e in items]
        return PagedResult(dto_items, total, page, page_size)

    async def Create(self, dto: UserDto) -> UserDto:
        """Tạo mới user từ DTO."""
        entity = MapperInstance.Map(dto, User)
        created = await self._unit_of_work.Users.Add(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(created, UserDto)

    async def Update(self, id: int, dto: UserDto) -> UserDto:
        """Cập nhật thông tin user theo Id."""
        entity = MapperInstance.Map(dto, User)
        entity.id = id
        updated = await self._unit_of_work.Users.Update(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(updated, UserDto)

    async def Delete(self, id: int) -> None:
        """Xoá user theo Id."""
        await self._unit_of_work.Users.Delete(id)
        await self._unit_of_work.SaveChanges()

    # -------- Current user helpers --------

    async def GetCurrentUserProfile(self, user_id: int) -> Optional[UserDto]:
        """Lấy thông tin profile của chính user."""
        return await self.GetById(user_id)

    async def GetCurrentUserRoles(self, user_id: int) -> List[str]:
        """Lấy danh sách role name của chính user."""
        roles = await self._unit_of_work.Roles.GetRolesByUser(user_id)
        return [r.name for r in roles]

    async def GetCurrentUserPermissions(self, user_id: int) -> List[str]:
        """
        Lấy danh sách permission name hiệu lực cho user
        (union tất cả permission của các role hiện tại).
        """
        roles = await self._unit_of_work.Roles.GetRolesByUser(user_id)
        perm_names: set[str] = set()
        for r in roles:
            perms = await self._unit_of_work.Permissions.GetPermissionsByRole(r.id)
            for p in perms:
                perm_names.add(p.name)
        return sorted(perm_names)

    async def UpdateCurrentUserRoles(self, user_id: int, role_names: List[str]) -> UserDto:
        """
        Cập nhật danh sách role cho chính user.

        - Clear toàn bộ roles cũ
        - Gán danh sách roles mới theo tên
        """
        roles = await self._unit_of_work.Roles.GetByNames(role_names)
        if len(roles) != len(set(role_names)):
            # Có tên role không tồn tại
            missing = set(role_names) - {r.name for r in roles}
            raise ValueError(f"Some roles not found: {', '.join(sorted(missing))}")

        # Clear & assign
        await self._unit_of_work.Roles.ClearRolesForUser(user_id)
        for r in roles:
            await self._unit_of_work.Roles.AssignRoleToUser(user_id=user_id, role_id=r.id)

        # Update cache on User entity
        entity = await self._unit_of_work.Users.GetById(user_id)
        if entity is None:
            raise ValueError("User not found when updating own roles")
        entity.roles = [r.name for r in roles]

        await self._unit_of_work.Users.Update(entity)
        await self._unit_of_work.SaveChanges()

        return MapperInstance.Map(entity, UserDto)

    async def ChangePassword(self, user_id: int, current_password: str, new_password: str) -> None:
        """
        Đổi mật khẩu cho user:

        - Kiểm tra current_password khớp với password_hash hiện tại
        - Hash new_password và lưu vào DB
        """
        from app.infrastructure.auth.PasswordHasher import VerifyPassword, HashPassword

        entity = await self._unit_of_work.Users.GetById(user_id)
        if entity is None:
            raise ValueError("User not found")

        if not entity.password_hash or not VerifyPassword(current_password, entity.password_hash):
            raise ValueError("Current password is incorrect")

        entity.password_hash = HashPassword(new_password)
        await self._unit_of_work.Users.Update(entity)
        await self._unit_of_work.SaveChanges()
