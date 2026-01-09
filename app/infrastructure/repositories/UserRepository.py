from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc

from app.domain.repositories.IUserRepository import IUserRepository
from app.domain.entities.User import User
from app.infrastructure.db.models.user_model import UserModel


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[User]:
        rows = self._session.query(UserModel).all()
        return [self._MapToEntity(r) for r in rows]

    async def GetById(self, id: int) -> Optional[User]:
        row = self._session.query(UserModel).filter(UserModel.Id == id).first()
        return self._MapToEntity(row) if row else None

    async def GetByUserName(self, user_name: str) -> Optional[User]:
        row = self._session.query(UserModel).filter(UserModel.UserName == user_name).first()
        print(row)
        return self._MapToEntity(row) if row else None

    async def Search(
        self,
        page: int,
        page_size: int,
        sort_by: str | None,
        sort_dir: str,
        search: str | None,
        is_active: bool | None,
    ) -> Tuple[List[User], int]:
        query = self._session.query(UserModel)

        if is_active is not None:
            query = query.filter(UserModel.IsActive == is_active)

        if search:
            like_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    UserModel.UserName.ilike(like_pattern),
                    UserModel.Email.ilike(like_pattern),
                    UserModel.FullName.ilike(like_pattern),
                )
            )

        sort_by = (sort_by or "Id").capitalize()
        sort_dir = (sort_dir or "asc").lower()

        sort_map = {
            "Id": UserModel.Id,
            "Username": UserModel.UserName,
            "UserName": UserModel.UserName,
            "Email": UserModel.Email,
            "Fullname": UserModel.FullName,
            "FullName": UserModel.FullName,
            "Isactive": UserModel.IsActive,
            "IsActive": UserModel.IsActive,
        }
        sort_column = sort_map.get(sort_by, UserModel.Id)

        if sort_dir == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        if page < 1:
            page = 1
        if page_size <= 0:
            page_size = 10

        total = query.count()
        rows = query.offset((page - 1) * page_size).limit(page_size).all()

        return [self._MapToEntity(r) for r in rows], total

    async def Add(self, entity: User) -> User:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.Id = row.Id
        return entity

    async def Update(self, entity: User) -> User:
        row = self._session.query(UserModel).filter(UserModel.Id == entity.Id).first()
        if not row:
            raise KeyError("User not found")
        row.UserName = entity.UserName
        row.Email = entity.Email
        row.FullName = entity.FullName
        row.IsActive = entity.IsActive
        row.PasswordHash = entity.PasswordHash
        row.Roles = self._Join(entity.Roles)
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(UserModel).filter(UserModel.Id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    def _MapToEntity(self, row: UserModel) -> User:
        return User(
            Id=row.Id,
            UserName=row.UserName,
            Email=row.Email,
            FullName=row.FullName,
            IsActive=row.IsActive,
            PasswordHash=row.PasswordHash,
            Roles=self._Split(row.Roles),
        )

    def _MapToModel(self, entity: User) -> UserModel:
        return UserModel(
            Id=entity.Id,
            UserName=entity.UserName,
            Email=entity.Email,
            FullName=entity.FullName,
            IsActive=entity.IsActive,
            PasswordHash=entity.PasswordHash,
            Roles=self._Join(entity.Roles),
        )

    def _Split(self, value: str | None) -> list[str] | None:
        if not value:
            return None
        return [x.strip() for x in value.split(",") if x.strip()]

    def _Join(self, items: list[str] | None) -> str | None:
        if not items:
            return None
        return ",".join(items)
