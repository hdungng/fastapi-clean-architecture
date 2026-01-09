from sqlalchemy.orm import Session

from app.infrastructure.db.base import SessionLocal, InitDb  # noqa: F401


class DbContext:
    """DbContext tương tự EF Core DbContext (quản lý SQLAlchemy Session)."""

    def __init__(self):
        self.Session: Session = SessionLocal()

    def Dispose(self):
        self.Session.close()
