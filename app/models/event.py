from sqlalchemy import Column, Integer, String, DateTime, Text
from app.models.base import Base
from datetime import datetime, timezone


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    event_type = Column(String, default="manual")  # 'manual' or other types

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', start={self.start})>"
