import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, local_test=False, load_from_db=False):
        self.LOCAL_TEST = local_test
        self.LOAD_FROM_DB = load_from_db

    API_KEY = os.getenv("API_KEY")
    API_SECRET_KEY = os.getenv("API_SECRET_KEY")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db:5432/twitter_db"
    )
    # Twitter Lists
    TWITTER_LIST_ID_SHITPOST = 1877782370352324758
    TWITTER_LIST_ID_AIRDROP = 1877785365790196202
    TWITTER_LIST_ID_AI = 1878005524123279870
    TWITTER_LIST_ID_STOCKS = 0000000000000000000
