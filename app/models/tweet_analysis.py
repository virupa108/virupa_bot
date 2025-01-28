from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class TweetBatchAnalysis(Base):
    __tablename__ = "tweet_batch_analysis"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    time_period = Column(String)  # e.g., "last_24h", "last_week"
    tweet_ids = Column(ARRAY(String))

    # Detailed analysis fields
    main_topics = Column(ARRAY(String))
    sentiment_summary = Column(JSON)  # Keeps JSON for nested structure like:
                                    # {"overall": "positive",
                                    #  "breakdown": {"positive": 0.6, ...}}
    key_insights = Column(ARRAY(String))
    trending_hashtags = Column(ARRAY(String))
    raw_llm_response = Column(Text)  # Store complete LLM response

    def __repr__(self):
        return f"<TweetBatchAnalysis(period={self.time_period}, timestamp={self.timestamp})>"