from dataclasses import dataclass
from datetime import datetime


@dataclass
class RefreshToken:
    user_id: int
    token: str
    expires_at: datetime
    id: int | None = None
    revoked_at: datetime | None = None
    replaced_by_token: str | None = None
    is_revoked: bool = False
