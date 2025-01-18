1. Use environment variables for DB credentials
Add indexes on frequently queried columns
3. Consider using async DB operations for better performance
Implement batch processing for LLM calls to save costs
Add error handling and retries for API calls
Would you like me to expand on any of these aspects?

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(String, primary_key=True)
    text = Column(String)
    created_at = Column(DateTime)
    author_id = Column(String)
    metrics = Column(JSON)
    list_id = Column(String, nullable=True)  # track which list it came from
    processed_by_llm = Column(Boolean, default=False)
    llm_response = Column(JSON, nullable=True)

# Update your main loop:
def process_tweets():
    engine = create_engine('postgresql://user:pass@localhost/dbname')
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        # Fetch from different lists
        for list_id in [TWITTER_LIST_ID_SHITPOST, TWITTER_LIST_ID_AIRDROP, TWITTER_LIST_ID_AI]:
            tweets = formatter.fetch_list_tweets(list_id)

            for tweet_data in tweets:
                # Check if tweet exists
                if not session.query(Tweet).filter_by(id=tweet_data['id']).first():
                    tweet = Tweet(**tweet_data, list_id=list_id)
                    session.add(tweet)

            session.commit()

        # Process unprocessed tweets with LLM
        unprocessed = session.query(Tweet).filter_by(processed_by_llm=False).limit(10)
        for tweet in unprocessed:
            # Call LLM API here
            # tweet.llm_response = llm_response
            # tweet.processed_by_llm = True

        session.commit()
        time.sleep(FETCH_INTERVAL)