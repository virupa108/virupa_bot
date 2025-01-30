import tweepy
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path
from rich.columns import Columns
from rich.markdown import Markdown
from rich.box import ROUNDED
from rich.style import Style
from rich import box
from textwrap import fill


class TweetFormatter:
    def __init__(
        self,
        client: tweepy.Client,
        cache_file: str = "sample_tweets.json",
        retweets=False,
    ) -> None:
        self.cache_file = Path(cache_file)
        self.console = Console()
        self.tweets = []
        self.client = client
        self.retweets = retweets
        self.last_tweet_id = None

    def fetch_tweets(self, count=15):
        """Fetch tweets from API and cache them"""
        try:  # try to fetch tweets
            response = self.client.get_home_timeline(
                max_results=count,
                since_id=self.last_tweet_id if self.last_tweet_id else None,
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
                exclude=(
                    [] if self.retweets else ["retweets"]
                ),  # Optional: exclude "retweets" or "replies" if you want
            )
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            return []

        if response.data:
            # update last_tweet_id
            self.last_tweet_id = response.data[0].id

        # Convert to serializable format
        tweets_data = self.convert_to_serializable(response)

        return tweets_data


    def save_tweets(self, tweets):
        """Save tweets to JSON file"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

    def load_tweets(self):
        """Load tweets from cache or fetch if needed"""
        if not self.cache_file.exists():
            print("Tweet cache not found, fetch tweets...")

        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def format_style(self, tweets):
        """Card style in single column with grouped metrics (based on style 3)"""

        def format_date(date):
            """Format date for display. Accepts both datetime object and ISO string"""
            if isinstance(date, str):
                dt = datetime.fromisoformat(date)
            else:
                dt = date  # Already a datetime object
            return dt.strftime("%b %d, %H:%M")

        def create_tweet_panel(tweet):
            # Create tweet URL
            username = tweet.author_username
            name = tweet.author_name
            tweet_id = tweet.tweet_id
            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
            tweet_text = tweet.text

            # Check if it's a retweet (text starts with "RT @")
            is_retweet = tweet_text.startswith("RT @")
            border_color = "red" if is_retweet else "cyan"

            # Header with user info
            header = f"[bold blue]{name}[/] " f"[cyan]@{username}[/]"

            engagement = (
                f"[link]{tweet_url}[/link]"  # Direct URL is more compatible
            )

            # Format content
            content = (
                f"{header}\n"
                f"[dim]{format_date(tweet.created_at)}[/]\n\n"
                f"{tweet_text}\n\n"
                f"{engagement}"
            )

            return Panel(
                content,
                border_style=border_color,
                padding=(1, 2),
                title="🔄 Retweet" if is_retweet else "🐦 Tweet",
                title_align="left",
                width=100,  # Fixed width for single column,
                box=box.ROUNDED,
            )

        # Create and display panels one by one
        for tweet in reversed(tweets):
            self.console.print(create_tweet_panel(tweet))
            # Add small spacing between tweets
            self.console.print("")
