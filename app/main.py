import tweepy
import colorama
from app.tweetformater import TweetFormatter
from app.utils.config import Config
from app.models.tweet import Base, Tweet
from app.database.session import engine, SessionLocal

db = SessionLocal()
colorama.init()

config = Config(local_test=False)
# config = Config(local_test=True, load_from_db=False)

client = tweepy.Client(
    bearer_token=config.BEARER_TOKEN,
    consumer_key=config.API_KEY,
    consumer_secret=config.API_SECRET_KEY,
    access_token=config.ACCESS_TOKEN,
    access_token_secret=config.ACCESS_TOKEN_SECRET,
)

formatter = TweetFormatter(client=client)
# fetch tweets and save to json
tweets_cache_file_exists = formatter.cache_file.exists()
if tweets_cache_file_exists and config.LOCAL_TEST:
    print("loading tweets from cache")
    tweets = formatter.load_tweets()
else:
    print("fetching tweets from API")
    # tweets = formatter.fetch_tweets()
    tweets = formatter.fetch_list_tweets(config.TWITTER_LIST_ID_SHITPOST)
    if not config.LOCAL_TEST:
        formatter.save_tweets(tweets)


formatter.format_style(tweets)
# Create tables
Base.metadata.create_all(bind=engine)

try:
    # Save tweets to db
    for tweet_data in tweets:
        tweet = Tweet(
            tweet_id=tweet_data['id'],
            text=tweet_data['text'],
            created_at=tweet_data['created_at'],
            author_id=tweet_data['author_id'],
            list_id=config.TWITTER_LIST_ID_SHITPOST,
        )
        db.add(tweet)
    db.commit()
finally:
    db.close()


# FETCH_INTERVAL = 300  # 5 minutes in seconds

# while True:
#     tweets = formatter.fetch_tweets()
#     Save to DB here instead?
#     or dont save and call openai API immidietly
#     formatter.save_tweets(tweets)
