def get_tweet_by_twitter_id(db, tweet_id: str):
    return db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()

def get_tweets_by_list(db, list_id: str):
    return db.query(Tweet).filter(Tweet.list_id == list_id).all()

def get_tweet_by_id(db, id: int):
    return db.query(Tweet).get(id)