from sqlalchemy import Column, Integer, String, DateTime, Text
from app.models.base import Base


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    summary_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    date_summarized = Column(DateTime, nullable=False)  # The date the tweets were from
