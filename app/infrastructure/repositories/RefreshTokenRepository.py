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
        entity.Id = row.Id
        return entity

    async def GetByToken(self, token: str) -> Optional[RefreshToken]:
        row = self._session.query(RefreshTokenModel).filter(RefreshTokenModel.Token == token).first()
        return self._MapToEntity(row) if row else None

    async def Revoke(self, token: RefreshToken) -> None:
        row = self._session.query(RefreshTokenModel).filter(RefreshTokenModel.Id == token.Id).first()
        if row:
            row.IsRevoked = True
            self._session.flush()

    async def RevokeAllForUser(self, user_id: int) -> None:
        rows = self._session.query(RefreshTokenModel).filter(
            and_(RefreshTokenModel.UserId == user_id, RefreshTokenModel.IsRevoked == False)  # noqa: E712
        )
        for row in rows:
            row.IsRevoked = True
        self._session.flush()

    async def GetValidTokensForUser(self, user_id: int) -> List[RefreshToken]:
        from datetime import datetime

        now = datetime.utcnow()
        rows = self._session.query(RefreshTokenModel).filter(
            and_(
                RefreshTokenModel.UserId == user_id,
                RefreshTokenModel.IsRevoked == False,  # noqa: E712
                RefreshTokenModel.ExpiresAt > now,
            )
        )
        return [self._MapToEntity(r) for r in rows]

    def _MapToEntity(self, row: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            Id=row.Id,
            UserId=row.UserId,
            Token=row.Token,
            ExpiresAt=row.ExpiresAt,
            RevokedAt=row.RevokedAt,
            ReplacedByToken=row.ReplacedByToken,
            IsRevoked=row.IsRevoked,
        )

    def _MapToModel(self, entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            Id=entity.Id,
            UserId=entity.UserId,
            Token=entity.Token,
            ExpiresAt=entity.ExpiresAt,
            RevokedAt=entity.RevokedAt,
            ReplacedByToken=entity.ReplacedByToken,
            IsRevoked=entity.IsRevoked,
        )
