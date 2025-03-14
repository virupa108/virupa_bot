from datetime import datetime, timedelta
import logging
import re
from typing import List
from openai import OpenAI
from app.repositories.tweet_repository import (
    get_tweets_by_date_range,
    get_dates_without_summaries,
)
from app.repositories.summary_repository import save_summary, get_summary_by_date
import time

logger = logging.getLogger(__name__)


class OpenAIService:  # Renamed from SummaryService
    def __init__(self, db, config):
        self.db = db
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.config = config

    def get_daily_summary(self, date: datetime = None) -> str:
        """
        Summarize tweets for a specific day using OpenAI
        Args:
            date: Date to summarize (defaults to today)
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
            # logger.info(f"Formatted tweets for prompt: {tweets_text}")

            # Generate prompt
            prompt = self._create_prompt(tweets_text)

            # Get summary from OpenAI
            prompt_config = self.config.OPENAI_PROMPT_CONFIG["DAILY_SUMMARY"]
            response = self.client.chat.completions.create(
                model=prompt_config["model"],
                temperature=prompt_config["temperature"],
                max_tokens=prompt_config["max_tokens"],
                messages=[{"role": prompt_config["messages_roles"], "content": prompt}],
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

    def _clean_tweet_text(self, text: str) -> str:
        """Clean tweet text for the prompt"""
        # Remove URLs to save tokens (optional)
        text = re.sub(r"http\S+", "[link]", text)
        # Remove unnecessary whitespace and newlines
        text = " ".join(text.split())
        # Remove all emojis
        text = re.sub(r"[^\w\s]", "", text)
        # Remove RT prefix
        text = re.sub(r"^RT @\w+:", "", text).strip()
        return text

    def _format_tweets_for_prompt(self, tweets: List) -> str:
        """Format tweets into a string for the prompt"""
        # Group tweets by list_id
        tweets_by_list = {}
        for tweet in tweets:
            list_name = self.config.TWITTER_LISTS_INFO.get(str(tweet.list_id), "Other")
            if list_name not in tweets_by_list:
                tweets_by_list[list_name] = []
            tweets_by_list[list_name].append(tweet)

        # Format tweets by list with optimized format
        formatted_sections = []
        for list_name, list_tweets in tweets_by_list.items():
            formatted_sections.append(f"\n- {list_name} List")
            # Sort by created_at for chronological order
            sorted_tweets = sorted(
                list_tweets, key=lambda x: x.created_at, reverse=True
            )

            for tweet in sorted_tweets:
                cleaned_text = self._clean_tweet_text(tweet.text)
                if not cleaned_text:  # empty text
                    continue
                formatted_sections.append(f"[@{tweet.author_username}] {cleaned_text}")

        return "\n".join(formatted_sections)

    def _create_prompt(self, tweets_text: str) -> str:
        """Create the prompt for OpenAI"""
        prompt = self.config.PROMPTS["DAILY_SUMMARY_PROMPT"]
        return prompt.format(tweets=tweets_text)

    def process_missing_summaries(self, max_days=None, delay_seconds=1):
        """
        Generate summaries for all dates that have tweets but no summaries
        Args:
            max_days: Optional limit on number of days to process, starting from most recent
            delay_seconds: Delay between API calls to respect rate limits
        """
        try:
            dates = get_dates_without_summaries(self.db)
            total_dates = len(dates) if not max_days else min(len(dates), max_days)

            logger.info(f"Found {total_dates} dates without summaries")

            # Process dates from most recent
            for i, date_row in enumerate(dates[:max_days] if max_days else dates):
                date = date_row.date
                logger.info(f"Processing summaries for {date} ({i+1}/{total_dates})")

                summary = self.get_daily_summary(date=date)
                if summary:
                    logger.info(f"Successfully generated summary for {date}")
                else:
                    logger.warning(f"Failed to generate summary for {date}")

                time.sleep(delay_seconds)

            logger.info("Completed processing historical summaries")

        except Exception as e:
            logger.error(f"Error in batch processing summaries: {str(e)}")
