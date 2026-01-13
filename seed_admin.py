"""Seed an admin user + default roles & permissions.

Usage:
    python seed_admin.py
"""

import asyncio

from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.db.base import InitDb
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.PasswordHasher import HashPassword
from app.domain.entities.Role import Role
from app.domain.entities.Permission import Permission


ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "123456"


async def seed():
    print("Initializing database...")
    InitDb()

    db = DbContext()
    uow = UnitOfWork(db)

    # 1) Seed roles
    default_roles = ["SuperAdmin", "Admin", "User"]
    role_entities: dict[str, Role] = {}
    for name in default_roles:
        existing = await uow.Roles.GetByName(name)
        if existing is None:
            created = await uow.Roles.Add(Role(Id=None, Name=name, Description=f"{name} role", IsActive=True))
            role_entities[name] = created
        else:
            role_entities[name] = existing

    # 2) Seed permissions
    default_permissions = [
        "Users.Read",
        "Users.Write",
        "Users.Self.ManageRoles",
        "Products.Read",
        "Products.Write",
        "Roles.Read",
        "Roles.Write",
        "Permissions.Read",
        "Permissions.Write",
    ]
    perm_entities: dict[str, Permission] = {}
    for name in default_permissions:
        existing = await uow.Permissions.GetByName(name)
        if existing is None:
            created = await uow.Permissions.Add(
                Permission(Id=None, Name=name, Description=f"{name} permission", IsActive=True)
            )
            perm_entities[name] = created
        else:
            perm_entities[name] = existing

    # 3) Grant all permissions to SuperAdmin
    super_admin_role = role_entities["SuperAdmin"]
    for p in perm_entities.values():
        await uow.Permissions.AssignPermissionToRole(permission_id=p.Id, role_id=super_admin_role.Id)

    # 4) Admin: subset (Users.*, Products.*)
    admin_role = role_entities["Admin"]
    for name in ["Users.Read", "Users.Write", "Products.Read", "Products.Write"]:
        p = perm_entities[name]
        await uow.Permissions.AssignPermissionToRole(permission_id=p.Id, role_id=admin_role.Id)

    # 5) User: read-only
    user_role = role_entities["User"]
    for name in ["Users.Read", "Products.Read"]:
        p = perm_entities[name]
        await uow.Permissions.AssignPermissionToRole(permission_id=p.Id, role_id=user_role.Id)

    # 6) Seed admin user
    existing_user = await uow.Users.GetByUserName(ADMIN_USERNAME)
    from app.domain.entities.User import User

    if existing_user is None:
        user = User(
            Id=None,
            UserName=ADMIN_USERNAME,
            Email=ADMIN_EMAIL,
            FullName="System Administrator",
            IsActive=True,
            PasswordHash=HashPassword(ADMIN_PASSWORD),
            Roles=None,
            Permissions=None,
        )
        created_user = await uow.Users.Add(user)
        user_id = created_user.Id
    else:
        user_id = existing_user.Id

    # 7) Assign SuperAdmin role to admin user
    await uow.Roles.AssignRoleToUser(user_id=user_id, role_id=super_admin_role.Id)

    # 8) Sync cached Roles & Permissions on User (denormalized)
    #    - Collect roles & permissions từ DB và lưu vào cột Users.Roles / Users.Permissions
    roles = await uow.Roles.GetRolesByUser(user_id)
    role_names = [r.Name for r in roles]

    # sum permissions từ tất cả role
    from app.infrastructure.db.models.role_permission_model import RolePermissionModel
    from app.infrastructure.db.models.permission_model import PermissionModel

    session = db.Session
    perm_rows = (
        session.query(PermissionModel)
        .join(RolePermissionModel, RolePermissionModel.permission_id == PermissionModel.id)
        .filter(RolePermissionModel.role_id.in_([r.Id for r in roles]))
        .all()
    )
    perm_names = sorted({p.Name for p in perm_rows})

    user_row = session.query(
        __import__("app.infrastructure.db.models.user_model", fromlist=["UserModel"]).UserModel
    ).filter_by(id=user_id).first()
    if user_row:
        user_row.roles = ",".join(role_names)
        session.flush()

    await uow.SaveChanges()

    print("=======================================")
    print("Admin user & default roles/permissions created/updated successfully!")
    print(f"UserName : {ADMIN_USERNAME}")
    print(f"Password : {ADMIN_PASSWORD}")
    print(f"Roles    : {role_names}")
    print(f"Perms    : {perm_names}")
    print("=======================================")


if __name__ == "__main__":
    asyncio.run(seed())
