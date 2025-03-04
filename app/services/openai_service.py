from datetime import datetime, timedelta
import logging
from typing import List
from openai import OpenAI
from app.repositories.tweet_repository import get_tweets_by_date_range
from app.repositories.summary_repository import save_summary, get_summary_by_date

logger = logging.getLogger(__name__)


class OpenAIService:  # Renamed from SummaryService
    def __init__(self, db, config):
        self.db = db
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.config = config

    def get_daily_summary(
        self, date: datetime = None, prompt_template: str = None
    ) -> str:
        """
        Summarize tweets for a specific day using OpenAI
        Args:
            date: Date to summarize (defaults to today)
            prompt_template: Custom prompt template for the summary
        """
        try:
            # Default to today if no date provided
            target_date = date or datetime.utcnow().date()
            start_date = datetime.combine(target_date, datetime.min.time())
            end_date = start_date + timedelta(days=1)

            # Check if summary already exists
            existing_summary = get_summary_by_date(self.db, start_date)
            if existing_summary:
                logger.info(f"Found existing summary for {target_date}")
                return existing_summary.summary_text

            # Get tweets for the date range
            tweets = get_tweets_by_date_range(self.db, start_date, end_date)

            if not tweets:
                logger.info(f"No tweets found for {target_date}")
                return None

            # Format tweets for the prompt
            tweets_text = self._format_tweets_for_prompt(tweets)

            # Generate prompt
            prompt = self._create_prompt(tweets_text, prompt_template)

            # Get summary from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",  # or gpt-3.5-turbo for faster/cheaper results
                messages=[
                    {"role": "system", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            summary = response.choices[0].message.content

            # Save the summary
            saved_summary = save_summary(self.db, summary, start_date)
            if saved_summary:
                logger.info(f"Saved summary for {target_date}")

            return summary

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return None

    def _format_tweets_for_prompt(self, tweets: List) -> str:
        """Format tweets into a string for the prompt"""
        # Group tweets by list_id
        tweets_by_list = {}
        for tweet in tweets:
            list_name = self.config.TWITTER_LISTS_INFO.get(str(tweet.list_id), "Other")
            if list_name not in tweets_by_list:
                tweets_by_list[list_name] = []
            tweets_by_list[list_name].append(tweet)

        # Format tweets by list
        formatted_sections = []
        for list_name, list_tweets in tweets_by_list.items():
            formatted_sections.append(f"\nTweets from List {list_name}:")
            for tweet in list_tweets:
                formatted_sections.append(
                    f"""
                    Tweet author:  {tweet.author_name} (@{tweet.author_username}).\n
                    Tweet content: \n{tweet.text}.\n
                    Tweet created at: {tweet.created_at}.
                    """
                )
        formated_llm_prompt = "\n".join(formatted_sections)
        return formated_llm_prompt

    def _create_prompt(self, tweets_text: str, custom_template: str = None) -> str:
        """Create the prompt for OpenAI"""
        default_template = """
        You are a professional investor and speculator content curator and summarizer. Analyze these tweets which are grouped by different Twitter lists.
        Each list has a different focus:
        - List Crypto Traders
        - List Airdrops
        - List Stocks
        and others etc.

        Ignore funny tweets, memes, jokes, satirical tweets, etc.

        Create a comprehensive summary organized by list categories.
        For List Crypto Traders tweets, focus on:
            Sentiment - Main topics and themes try to identify user's sentiment, example: @userA is bullish on BTC, @userB is frustrated or bearish on ETH
            Insights - Key insights and important information
            Updates - Fundamental project/protocol updates or changes
            Emerging trends - Emerging trends
            New projects - New projects investments in stocks or crypto
            Events - reminder of Important future events, token unlocks, macro events such as FED meetings, big option expirations, stock earnings, CPI prints

        For list Airdrops tweets, focus on:
           Deadlines -  Crypto Airdrop deadline claims or task deadlines, deadlines for snapshots etc. even for NFTs
           Tasks - reminder of tasks to complete for airdrop
           New airdrops - new airdrops to watch out for

        For list Stocks tweets, focus on:
            Mentioned stocks - mentioned stocks on the timeline their name ticker and reason of mention
            Earnings - earnings announcements and information
            Speculation - such as short interest, analyst calls, etc

        List Crypto Traders:
            Sentiment - "<analysis here>"
            Insights - "<analysis here>"
            Updates - "<analysis here>"
            Emerging trends - "<analysis here>"
            New projects - "<analysis here>"
            Events - "<analysis here>"

        etc.. same for other lists

        Tweets to analyze:

        {tweets}
        """

        template = custom_template or default_template
        return template.format(tweets=tweets_text)
