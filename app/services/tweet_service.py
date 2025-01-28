from sqlalchemy.exc import IntegrityError
from app.models.tweet import Tweet

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