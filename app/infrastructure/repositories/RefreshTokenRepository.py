from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.domain.repositories.IRefreshTokenRepository import IRefreshTokenRepository
from app.domain.entities.RefreshToken import RefreshToken
from app.infrastructure.db.models.refresh_token_model import RefreshTokenModel
from app.infrastructure.mapping.AutoMapper import MapperInstance


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: Session):
        self._session = session

    async def Add(self, entity: RefreshToken) -> RefreshToken:
        row = MapperInstance.Map(entity, RefreshTokenModel)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def GetByToken(self, token: str) -> Optional[RefreshToken]:
        row = self._session.query(RefreshTokenModel).filter(RefreshTokenModel.token == token).first()
        return MapperInstance.Map(row, RefreshToken) if row else None

    async def Revoke(self, token: RefreshToken) -> None:
        row = self._session.query(RefreshTokenModel).filter(RefreshTokenModel.id == token.id).first()
        if row:
            row.is_revoked = True
            self._session.flush()

    async def RevokeAllForUser(self, user_id: int) -> None:
        rows = self._session.query(RefreshTokenModel).filter(
            and_(RefreshTokenModel.user_id == user_id, RefreshTokenModel.is_revoked == False)  # noqa: E712
        )
        for row in rows:
            row.is_revoked = True
        self._session.flush()

    async def GetValidTokensForUser(self, user_id: int) -> List[RefreshToken]:
        from datetime import datetime

        now = datetime.utcnow()
        rows = self._session.query(RefreshTokenModel).filter(
            and_(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.is_revoked == False,  # noqa: E712
                RefreshTokenModel.expires_at > now,
            )
        )
        return [MapperInstance.Map(r, RefreshToken) for r in rows]
