import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, local_test=False, load_from_db=False):
        self.LOCAL_TEST = local_test
        self.LOAD_FROM_DB = load_from_db

    FRED_API_KEY = os.getenv("FRED_API_KEY")
    FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

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
    # Critical events

    CRITICAL_EVENTS = {
        "USA": {
            "FED": {
                "2025-01-29T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-03-19T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-05-07T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-06-18T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-07-30T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-09-17T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-10-29T18:30:00Z": "FOMC Meeting + Rate Decision",
                "2025-12-10T18:30:00Z": "FOMC Meeting + Rate Decision",
            },
            "CPI": {
                "2025-01-15T12:30:00Z": "Consumer Price Index Release",
                "2025-02-12T12:30:00Z": "Consumer Price Index Release",
                "2025-03-12T12:30:00Z": "Consumer Price Index Release",
                "2025-04-10T12:30:00Z": "Consumer Price Index Release",
                "2025-05-13T12:30:00Z": "Consumer Price Index Release",
                "2025-06-11T12:30:00Z": "Consumer Price Index Release",
                "2025-07-15T12:30:00Z": "Consumer Price Index Release",
                "2025-08-12T12:30:00Z": "Consumer Price Index Release",
                "2025-09-11T12:30:00Z": "Consumer Price Index Release",
                "2025-10-15T12:30:00Z": "Consumer Price Index Release",
                "2025-11-13T12:30:00Z": "Consumer Price Index Release",
                "2025-12-10T12:30:00Z": "Consumer Price Index Release",
            },
            "GDP": {
                "2025-01-30T12:30:00Z": "GDP Release (Advance Estimate)",
                "2025-02-27T12:30:00Z": "GDP Release (Second Estimate)",
                "2025-03-27T12:30:00Z": "GDP Release (Third Estimate)",
                "2025-04-30T12:30:00Z": "GDP Release (Advance Estimate)",
                "2025-05-29T12:30:00Z": "GDP Release (Second Estimate)",
                "2025-06-26T12:30:00Z": "GDP Release (Third Estimate)",
                "2025-07-30T12:30:00Z": "GDP Release (Advance Estimate)",
                "2025-08-28T12:30:00Z": "GDP Release (Second Estimate)",
                "2025-09-25T12:30:00Z": "GDP Release (Third Estimate)",
                "2025-10-30T12:30:00Z": "GDP Release (Advance Estimate)",
                "2025-11-26T12:30:00Z": "GDP Release (Second Estimate)",
                "2025-12-19T12:30:00Z": "GDP Release (Third Estimate)",
            },
            "Unemployment": {
                "2025-01-10T12:30:00Z": "Employment Situation Release",
                "2025-02-07T12:30:00Z": "Employment Situation Release",
                "2025-03-07T12:30:00Z": "Employment Situation Release",
                "2025-04-04T12:30:00Z": "Employment Situation Release",
                "2025-05-02T12:30:00Z": "Employment Situation Release",
                "2025-06-06T12:30:00Z": "Employment Situation Release",
                "2025-07-03T12:30:00Z": "Employment Situation Release",
                "2025-08-01T12:30:00Z": "Employment Situation Release",
                "2025-09-05T12:30:00Z": "Employment Situation Release",
                "2025-10-03T12:30:00Z": "Employment Situation Release",
                "2025-11-07T12:30:00Z": "Employment Situation Release",
                "2025-12-05T12:30:00Z": "Employment Situation Release",
            },
        },
        "EU": {
            "ECB": {
                "2025-01-30T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-03-06T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-04-17T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-06-05T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-07-24T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-09-11T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-10-30T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
                "2025-12-18T13:15:00Z": "ECB Monetary Policy Meeting + Rate Decision",
            },
            "CPI": {
                "2025-01-17T12:00:00Z": "Euro Area Inflation Rate Release",
                "2025-02-21T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-03-20T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-04-17T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-05-22T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-06-19T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-07-17T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-08-21T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-09-18T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-10-16T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-11-20T12:30:00Z": "Euro Area Inflation Rate Release",
                "2025-12-18T12:30:00Z": "Euro Area Inflation Rate Release",
            },
            "GDP": {
                "2025-02-14T12:30:00Z": "Preliminary Flash Estimate of GDP Growth",
                "2025-03-07T12:30:00Z": "Flash Estimate of GDP and Employment Growth",
                "2025-05-15T12:30:00Z": "Preliminary Flash Estimate of GDP Growth",
                "2025-06-06T12:30:00Z": "Flash Estimate of GDP and Employment Growth",
                "2025-08-14T12:30:00Z": "Preliminary Flash Estimate of GDP Growth",
                "2025-09-05T12:30:00Z": "Flash Estimate of GDP and Employment Growth",
                "2025-11-14T12:30:00Z": "Preliminary Flash Estimate of GDP Growth",
                "2025-12-05T12:30:00Z": "Flash Estimate of GDP and Employment Growth",
            },
            "Unemployment": {
                "2025-01-31T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-02-28T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-03-31T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-04-30T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-05-30T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-06-30T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-07-31T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-08-29T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-09-30T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-10-31T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-11-28T12:30:00Z": "Euro Area Unemployment Rate Release",
                "2025-12-31T12:30:00Z": "Euro Area Unemployment Rate Release",
            },
        },
    }
