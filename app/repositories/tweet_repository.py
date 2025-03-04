from app.models.tweet import Tweet
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_tweets(db, limit: int = 500):
    return db.query(Tweet).order_by(Tweet.tweet_id.desc()).limit(limit).all()


def get_tweet_by_twitter_id(db, tweet_id: str):
    return db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()


def get_tweets_by_list(db, list_id: str):
    return db.query(Tweet).filter(Tweet.list_id == list_id).all()


def get_tweet_by_id(db, id: int):
    return db.query(Tweet).get(id)


def get_latest_tweet_id_by_list(db, list_id) -> str:
    """
    Get the most recent tweet_id for a specific list.
    """
    try:
        latest_tweet = (
            db.query(Tweet)
            .filter(Tweet.list_id == str(list_id))
            .order_by(Tweet.tweet_id.desc())
            .first()
        )
        return latest_tweet.tweet_id if latest_tweet else None

    except Exception as e:
        logger.error(f"Error getting latest tweet_id: {str(e)}")
        return None


def get_recent_tweets(db, list_id: str, limit: int = 20):
    """
    Get the most recent tweets for a specific list.
    Args:
        db: Database session
        list_id: ID of the list to fetch from
        limit: Maximum number of tweets to fetch (default 20)
    Returns:
        List of Tweet objects
    """
    try:
        tweets = (
            db.query(Tweet)
            .filter(Tweet.list_id == str(list_id))
            .order_by(Tweet.tweet_id.desc())
            .limit(limit)
            .all()
        )
        logger.info(f"Fetched {len(tweets)} recent tweets from database")
        return tweets
    except Exception as e:
        logger.error(f"Error fetching recent tweets: {str(e)}")
        return []


def get_tweets_by_date_range(db, start_date: datetime, end_date: datetime):
    """Get tweets between two dates"""
    return (
        db.query(Tweet)
        .filter(Tweet.created_at >= start_date)
        .filter(Tweet.created_at < end_date)
        .order_by(Tweet.created_at.desc())
        .all()
    )
