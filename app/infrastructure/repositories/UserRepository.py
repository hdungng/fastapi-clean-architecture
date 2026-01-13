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
        row = self._session.query(UserModel).filter(UserModel.id == id).first()
        return self._MapToEntity(row) if row else None

    async def GetByUserName(self, user_name: str) -> Optional[User]:
        row = self._session.query(UserModel).filter(UserModel.user_name == user_name).first()
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
            query = query.filter(UserModel.is_active == is_active)

        if search:
            like_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    UserModel.user_name.ilike(like_pattern),
                    UserModel.email.ilike(like_pattern),
                    UserModel.full_name.ilike(like_pattern),
                )
            )

        sort_key = (sort_by or "id").lower()
        sort_dir = (sort_dir or "asc").lower()

        sort_map = {
            "id": UserModel.id,
            "username": UserModel.user_name,
            "user_name": UserModel.user_name,
            "email": UserModel.email,
            "fullname": UserModel.full_name,
            "full_name": UserModel.full_name,
            "isactive": UserModel.is_active,
            "is_active": UserModel.is_active,
        }
        sort_column = sort_map.get(sort_key, UserModel.id)

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
        entity.id = row.id
        return entity

    async def Update(self, entity: User) -> User:
        row = self._session.query(UserModel).filter(UserModel.id == entity.id).first()
        if not row:
            raise KeyError("User not found")
        row.user_name = entity.user_name
        row.email = entity.email
        row.full_name = entity.full_name
        row.is_active = entity.is_active
        row.password_hash = entity.password_hash
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(UserModel).filter(UserModel.id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    def _MapToEntity(self, row: UserModel) -> User:
        return User(
            id=row.id,
            user_name=row.user_name,
            email=row.email,
            full_name=row.full_name,
            is_active=row.is_active,
            password_hash=row.password_hash,
            roles=None,
        )

    def _MapToModel(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            user_name=entity.user_name,
            email=entity.email,
            full_name=entity.full_name,
            is_active=entity.is_active,
            password_hash=entity.password_hash,
        )
