from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tweet_id = Column(String, unique=True, nullable=False, index=True)
    text = Column(String)
    created_at = Column(DateTime)
    author_id = Column(String)
    list_id = Column(String)
    author_username = Column(String)
    author_name = Column(String)

    def __repr__(self):
        return f"<Tweet(id={self.id}, tweet_id={self.tweet_id}, author_id={self.author_id})>"
