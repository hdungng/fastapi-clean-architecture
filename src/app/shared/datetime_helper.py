from datetime import datetime, timezone


def UtcNow() -> datetime:
    return datetime.now(timezone.utc)


def FormatIso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()
