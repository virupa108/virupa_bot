import tweepy
import colorama
from app.tweetformater import TweetFormatter
from app.utils.config import Config
from app.models.tweet import Base, Tweet
from app.database.session import engine, SessionLocal
from app.services.tweet_service import update_list_tweets
from app.repositories.tweet_repository import get_recent_tweets, get_tweets_by_list, get_tweets
from app.utils import setup_logger

# Set up logging with colors
logger = setup_logger()

# Initialize database and colorama
db = SessionLocal()
colorama.init()

def main():
    try:
        # Initialize config and Twitter client
        config = Config(local_test=True)
        client = tweepy.Client(
            bearer_token=config.BEARER_TOKEN,
            consumer_key=config.API_KEY,
            consumer_secret=config.API_SECRET_KEY,
            access_token=config.ACCESS_TOKEN,
            access_token_secret=config.ACCESS_TOKEN_SECRET,
        )

        # Create database tables if they don't exist
        Base.metadata.create_all(bind=engine)

        # Initialize formatter for display
        formatter = TweetFormatter(client=client)

        if not config.LOCAL_TEST:
            # In local test mode, just fetch from DB
            # Normal mode - fetch from API and update DB
            logger.info("--- Fetching new tweets from API ---")
            for list_id in config.TWITTER_LISTS:
                new_tweets_count = update_list_tweets(
                    client=client,
                    db=db,
                    list_id=list_id
                )
            logger.info(f"--- Saved {new_tweets_count} new tweets ---")

        # Get all tweets for display
        display_tweets = get_tweets(db=db, limit=5)

        # Display tweets using formatter
        if display_tweets:
            logger.info(f"--- Displaying {len(display_tweets)} tweets ---")
            formatter.format_style(display_tweets)
        else:
            logger.info("--- No tweets to display, database is empty ---")

    except Exception as e:
        logger.error(f"--- Error in main: {str(e)} ---")
    finally:
        db.close()

if __name__ == "__main__":
    main()
