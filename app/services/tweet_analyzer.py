from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from app.models.tweet import Tweet
from app.models.tweet_analysis import TweetBatchAnalysis

class TweetAnalyzer:
    def __init__(self, db_session, llm_client):
        self.db = db_session
        self.llm = llm_client

    def get_unprocessed_tweets(self, hours: int) -> List[Tweet]:
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        return self.db.query(Tweet)\
            .filter(Tweet.created_at >= cutoff)\
            .filter(Tweet.processed_by_llm == False)\
            .all()

    def prepare_tweets_for_analysis(self, tweets: List[Tweet]) -> str:
        # Format tweets in a way that's optimal for LLM analysis
        formatted_tweets = []
        for tweet in tweets:
            formatted_tweets.append(f"Tweet {tweet.id}: {tweet.text}")
        return "\n".join(formatted_tweets)

    def create_analysis_prompt(self, formatted_tweets: str, hours: int) -> str:
        return f"""Analyze these tweets from the last {hours} hours and provide a structured analysis.

        Tweets:
        {formatted_tweets}

        Please provide analysis in the following JSON format:
        {{
            "main_topics": ["topic1", "topic2", ...],
            "sentiment_summary": {{
                "overall": "positive/negative/neutral",
                "breakdown": {{
                    "positive": percentage,
                    "negative": percentage,
                    "neutral": percentage
                }}
            }},
            "key_insights": [
                "insight1",
                "insight2",
                ...
            ],
            "trending_hashtags": ["hashtag1", "hashtag2", ...],
            "detailed_analysis": "comprehensive analysis text"
        }}
        """

    def analyze_tweets(self, hours: int = 24) -> Dict[str, Any]:
        tweets = self.get_unprocessed_tweets(hours)

        if not tweets:
            return None

        formatted_tweets = self.prepare_tweets_for_analysis(tweets)
        prompt = self.create_analysis_prompt(formatted_tweets, hours)

        # Get LLM response
        llm_response = self.llm.analyze(prompt)

        # Parse LLM response (assuming it returns JSON)
        try:
            analysis_data = json.loads(llm_response)
        except json.JSONDecodeError:
            # Handle non-JSON response
            analysis_data = {
                "error": "Failed to parse LLM response",
                "raw_response": llm_response
            }

        # Create analysis record
        analysis = TweetBatchAnalysis(
            time_period=f"last_{hours}h",
            tweet_ids=[t.id for t in tweets],
            main_topics=analysis_data.get("main_topics", []),
            sentiment_summary=analysis_data.get("sentiment_summary", {}),
            key_insights=analysis_data.get("key_insights", []),
            trending_hashtags=analysis_data.get("trending_hashtags", []),
            raw_llm_response=llm_response
        )

        # Update tweets as processed
        for tweet in tweets:
            tweet.processed_by_llm = True

        # Save to database
        self.db.add(analysis)
        self.db.commit()

        return analysis