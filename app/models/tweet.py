from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(String, primary_key=True)
    text = Column(String)
    created_at = Column(DateTime)
    author_id = Column(String)
    metrics = Column(JSON)
    list_id = Column(String)
    processed_by_llm = Column(Boolean, default=False)
    llm_response = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Tweet(id={self.id}, author_id={self.author_id})>"
