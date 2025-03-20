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
    TWITTER_LIST_ID_TRADERS = 1877782370352324758
    TWITTER_LIST_ID_AIRDROP = 1877785365790196202
    TWITTER_LIST_ID_AI = 1878005524123279870
    TWITTER_LIST_ID_STOCKS = 0000000000000000000

    TWITTER_LISTS = [
        TWITTER_LIST_ID_TRADERS,
        TWITTER_LIST_ID_AIRDROP,
        TWITTER_LIST_ID_STOCKS,
    ]

    # Twitter Lists with names
    TWITTER_LISTS_INFO = {
        TWITTER_LIST_ID_TRADERS: "CryptoTraders",
        TWITTER_LIST_ID_AIRDROP: "Airdrops",
        TWITTER_LIST_ID_AI: "AI",
        TWITTER_LIST_ID_STOCKS: "Stocks",
    }

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # OpenAI Configuration
    OPENAI_PROMPT_CONFIG = {
        "DAILY_SUMMARY": {
            # "model": "gpt-3.5-turbo-16k",
            "model": "gpt-4-1106-preview",  # gpt-4-turbo-preview is an alias for gpt-4-1106-preview, which is the latest GPT-4 model with 128k context window and lower pricing
            "temperature": 0.2,  # higher temp more creative response lower temp more determinsitc
            "max_tokens": 3000,  # Increased to maximum recommended
            "messages_roles": "system",
        }
    }

    # OpenAI Prompts
    PROMPTS = {
        "DAILY_SUMMARY_PROMPT": """You are a professional investor speculator. Analyze tweets by list categories.
        Lists have a different focus: - List Crypto Traders - List Airdrops - List Stocks.
        I'm only interested in the tweets relevant to the list. I want to always know about potential new narratives forming.
        Create a comprehensive summary organized by list categories. as in format below
        For Crypto Traders:
            Insights - Key insights and important information, @userA is bullish on BTC
            New projects - emerging trend, new projects investments, Fundamental project/protocol updates changes
            Events - Important future events, token unlocks, macro events :FED meetings, option expirations, earnings, CPI prints
        Airdrops:
           Deadlines -  Crypto/NFT Airdrop deadline claims, deadlines for tasks/snapshots
           Tasks - reminder of airdrop tasks
           New airdrops - new airdrops to follow
        Stocks:
            Mentioned stocks - stocks on the timeline, name ticker and reason of mention
            Earnings - earnings announcements
            Speculation - short interest, analyst calls
        Tweets to analyze:
        {tweets}
        """
    }
