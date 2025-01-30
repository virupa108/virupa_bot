from sqlalchemy.exc import IntegrityError
from app.models.tweet import Tweet
from app.repositories.tweet_repository import get_latest_tweet_id_by_list
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

def save_tweet(db, tweet_data):
    try:
        tweet = Tweet(
            tweet_id=str(tweet_data.id),  # Make sure it's a string
            text=tweet_data.text,
            created_at=tweet_data.created_at,
            author_id=str(tweet_data.author_id),
            list_id=str(tweet_data.list_id)
        )
        db.add(tweet)
        db.commit()
        return tweet
    except IntegrityError:
        db.rollback()
        # Tweet already exists
        return db.query(Tweet).filter(Tweet.tweet_id == str(tweet_data.id)).first()

def fetch_list_tweets(client, list_id: str, since_id: str = None, limit: int = None) -> list:
    """
    Fetch tweets from a list.
    Args:
        client: Twitter API client
        list_id: ID of the list to fetch from
        since_id: Only return tweets newer than this ID
        limit: Maximum number of tweets to fetch (None for no limit)
    """
    try:
        all_tweets = []
        all_users = {}
        last_response = None # store for the user data
        pagination_token = None
        retry_count = 0
        max_retries = 3
        wait_time = 2  # Initial wait time in seconds

        while True:
            try:
                response = client.get_list_tweets(
                    id=list_id,
                    pagination_token=pagination_token,
                    max_results=100,
                    tweet_fields=[
                        "created_at",
                        "public_metrics",
                        "author_id",
                        "text",
                        "conversation_id",
                        "in_reply_to_user_id",
                        "referenced_tweets",
                        "attachments",
                    ],
                    user_fields=["username", "name"],
                    expansions=["author_id", "referenced_tweets.id"]
                )

                if not response.data:
                    break

                # Collect users from this page
                if response.includes and 'users' in response.includes:
                    for user in response.includes['users']:
                        all_users[user.id] = user

                # If since_id is provided, filter tweets in memory
                if since_id:
                    new_tweets = [t for t in response.data if int(t.id) > int(since_id)]
                    if not new_tweets:
                        # If no new tweets in this batch, we can stop
                        break
                    all_tweets.extend(new_tweets)
                else:
                    all_tweets.extend(response.data)

                logger.info(f"Fetched batch of {len(response.data)} tweets")

                # Break if we've reached the limit
                if limit and len(all_tweets) >= limit:
                    all_tweets = all_tweets[:limit]  # Trim to exact limit
                    break

                pagination_token = response.meta.get('next_token')
                if not pagination_token:
                    break

                # Sleep between requests to avoid rate limits
                logger.info(f"Waiting {wait_time} seconds before next request...")
                time.sleep(wait_time)

            except Exception as e:
                logger.error(f"Error in request: {str(e)}")
                retry_count += 1
                if retry_count > max_retries:
                    logger.error("Max retries exceeded")
                    break

                wait_time *= 2  # Double the wait time for next retry
                continue

        logger.info(f"Fetched total of {len(all_tweets)} tweets from list {list_id}")

        return {
            "tweets": all_tweets,
            "includes": { # to keep twitter api format
                "users": all_users
            }
        }

    except Exception as e:
        logger.error(f"Error fetching tweets for list {list_id}: {str(e)}")
        return []

def update_list_tweets(client, db, list_id: str):
    """
    Update tweets from a list. If DB is empty, fetch initial batch.
    Returns number of new tweets saved.
    """
    since_id = get_latest_tweet_id_by_list(db, list_id)

    if not since_id:
        logger.info("No tweets in DB, fetching initial batch...")
        response = fetch_list_tweets(client, list_id, limit=100)  # Limit to 100 tweets, for initial load
    else:
        logger.info(f"Fetching tweets since ID: {since_id}")
        response = fetch_list_tweets(client, list_id, since_id)

    if not response:
        return 0

    try:
        tweets_data = convert_to_serializable(response)

        new_tweets = [
            Tweet(
                tweet_id=str(tweet["id"]),
                text=tweet["text"],
                created_at=tweet["created_at"],
                author_id=tweet["author_id"],
                author_username=tweet["author_username"],
                author_name=tweet["author_name"],
                list_id=str(list_id)
            )
            for tweet in tweets_data
        ]

        db.bulk_save_objects(new_tweets)
        db.commit()
        return len(new_tweets)

    except Exception as e:
        logger.error(f"Database error while saving tweets: {str(e)}", exc_info=True)
        db.rollback()
        return 0

# convert tweets to serializable format for JSON
def convert_to_serializable(response):
    """Convert tweets to serializable format for JSON"""

    users = response["includes"]["users"]
    tweets = response["tweets"]

    return [
        {
            "id": str(tweet.id),
            "text": tweet.text,
            "created_at": tweet.created_at.isoformat(),
            "author_id": str(tweet.author_id),
            "author_username": users[tweet.author_id].username,
            "author_name": users[tweet.author_id].name
        }
        for tweet in tweets
    ]

def fetch_home_timeline(client, since_id: str = None, exclude_retweets: bool = True) -> list:
    """
    Fetch tweets from home timeline.
    Args:
        client: Twitter API client
        since_id: Only return tweets newer than this ID
        exclude_retweets: Whether to exclude retweets from results
    Returns:
        List of tweets
    """
    try:
        all_tweets = []
        pagination_token = None

        while True:
            response = client.get_home_timeline(
                since_id=since_id,
                max_results=100,
                pagination_token=pagination_token,
                tweet_fields=[
                    "created_at",
                    "public_metrics",
                    "author_id",
                    "text",
                    "conversation_id",
                    "in_reply_to_user_id",
                    "referenced_tweets",
                    "attachments",
                ],
                user_fields=["username", "name"],
                expansions=["author_id", "referenced_tweets.id"],
                exclude=["retweets"] if exclude_retweets else []
            )

            if not response.data:
                break

            all_tweets.extend(response.data)

            pagination_token = response.meta.get('next_token')
            if not pagination_token:
                break

        logger.info(f"Fetched {len(all_tweets)} tweets from home timeline")
        return all_tweets

    except Exception as e:
        logger.error(f"Error fetching home timeline: {str(e)}")
        return []