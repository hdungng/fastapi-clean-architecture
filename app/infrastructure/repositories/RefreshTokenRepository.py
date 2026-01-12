from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.domain.repositories.IRefreshTokenRepository import IRefreshTokenRepository
from app.domain.entities.RefreshToken import RefreshToken
from app.infrastructure.db.models.refresh_token_model import RefreshTokenModel


class RefreshTokenRepository(IRefreshTokenRepository):
    def __init__(self, session: Session):
        self._session = session

    async def Add(self, entity: RefreshToken) -> RefreshToken:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def GetByToken(self, token: str) -> Optional[RefreshToken]:
        row = self._session.query(RefreshTokenModel).filter(RefreshTokenModel.token == token).first()
        return self._MapToEntity(row) if row else None

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
        return [self._MapToEntity(r) for r in rows]

    def _MapToEntity(self, row: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=row.id,
            user_id=row.user_id,
            token=row.token,
            expires_at=row.expires_at,
            revoked_at=row.revoked_at,
            replaced_by_token=row.replaced_by_token,
            is_revoked=row.is_revoked,
        )

    def _MapToModel(self, entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token=entity.token,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
            replaced_by_token=entity.replaced_by_token,
            is_revoked=entity.is_revoked,
        )
