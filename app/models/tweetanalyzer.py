# import tweepy
# import openai
# from datetime import datetime, timedelta
# import json
# import sqlite3
# from collections import defaultdict


# analyzer = TweetAnalyzer()

# # Run hourly via cron/scheduler
# summary = analyzer.hourly_run()
# print(summary)

# Tips to reduce costs:
# Batch tweets before sending to OpenAI
# Use GPT-3.5-turbo instead of GPT-4
# Pre-filter tweets before sending to OpenAI
# Store summaries locally
# Consider local open-source models like LlamaCpp for processing

# Storage/Processing:
# SQLite for local storage
# Track processed tweets
# Store summaries for reference

# class TweetAnalyzer:
#     def __init__(self):
#         self.client = tweepy.Client(bearer_token="YOUR_BEARER_TOKEN")
#         openai.api_key = "YOUR_OPENAI_KEY"
#         self.setup_db()

#     def setup_db(self):
#         """Store processed tweets to avoid reprocessing"""
#         self.conn = sqlite3.connect("tweets.db")
#         self.conn.execute(
#             """CREATE TABLE IF NOT EXISTS tweets
#             (id TEXT PRIMARY KEY, content TEXT, processed INTEGER)"""
#         )
#         self.conn.execute(
#             """CREATE TABLE IF NOT EXISTS summaries
#             (date TEXT PRIMARY KEY, summary TEXT)"""
#         )

#     def pre_filter_tweets(self, tweets):
#         """First level of filtering to reduce OpenAI API usage"""
#         important_tweets = []

#         # Keywords that matter to you
#         keywords = ["ai", "tech", "breaking", "launch", "announcement"]

#         for tweet in tweets:
#             # Skip if already processed
#             if self.is_processed(tweet.id):
#                 continue

#             text = tweet.text.lower()

#             # Score tweet importance
#             score = 0
#             score += tweet.public_metrics["like_count"] * 0.1
#             score += tweet.public_metrics["retweet_count"] * 0.3
#             score += any(k in text for k in keywords) * 10

#             if score > 5:  # Threshold for "importance"
#                 important_tweets.append(
#                     {
#                         "id": tweet.id,
#                         "text": tweet.text,
#                         "metrics": tweet.public_metrics,
#                         "score": score,
#                     }
#                 )

#         return important_tweets

#     def batch_process(self, tweets, batch_size=20):
#         """Process tweets in optimal batches for OpenAI"""
#         summaries = []

#         for i in range(0, len(tweets), batch_size):
#             batch = tweets[i : i + batch_size]

#             # Construct efficient prompt
#             prompt = self.create_efficient_prompt(batch)

#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": """
#                          Analyze tweets and extract only critically important info.
#                          Format:
#                          - [BREAKING/TECH/AI]: Brief summary
#                          Skip everything that isn't truly noteworthy.
#                          """,
#                         },
#                         {"role": "user", "content": prompt},
#                     ],
#                     temperature=0.3,  # Lower temperature for more focused output
#                 )

#                 summaries.append(response.choices[0].message["content"])

#                 # Mark these tweets as processed
#                 self.mark_processed([t["id"] for t in batch])

#             except Exception as e:
#                 print(f"Error processing batch: {e}")
#                 continue

#         return "\n".join(summaries)

#     def create_efficient_prompt(self, tweets):
#         """Create token-efficient prompt"""
#         return "\n".join(
#             [
#                 f"Likes:{t['metrics']['like_count']} RTs:{t['metrics']['retweet_count']} - {t['text'][:200]}"
#                 for t in tweets
#             ]
#         )

#     def hourly_run(self):
#         """Main function to run every hour"""

#         # Get tweets since last run
#         last_run = self.get_last_run_time()
#         tweets = self.get_new_tweets(last_run)

#         # Pre-filter
#         important_tweets = self.pre_filter_tweets(tweets)

#         if not important_tweets:
#             return "No important updates"

#         # Process in batches
#         summary = self.batch_process(important_tweets)

#         # Store summary
#         self.store_summary(summary)

#         return summary

#     def is_processed(self, tweet_id):
#         """Check if tweet was already processed"""
#         cursor = self.conn.execute("SELECT 1 FROM tweets WHERE id = ?", (tweet_id,))
#         return cursor.fetchone() is not None

#     def mark_processed(self, tweet_ids):
#         """Mark tweets as processed"""
#         self.conn.executemany(
#             "INSERT OR IGNORE INTO tweets (id, processed) VALUES (?, 1)",
#             [(id,) for id in tweet_ids],
#         )
#         self.conn.commit()
