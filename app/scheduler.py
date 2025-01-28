from celery import Celery
from app.services.tweet_analyzer import TweetAnalyzer
from app.database import SessionLocal
from app.llm_client import LLMClient

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def run_tweet_analysis(hours: int = 24):
    db = SessionLocal()
    llm_client = LLMClient()  # Your LLM client implementation

    try:
        analyzer = TweetAnalyzer(db, llm_client)
        analysis = analyzer.analyze_tweets(hours)
        return f"Analysis completed. ID: {analysis.id if analysis else 'No tweets to analyze'}"
    finally:
        db.close()

# Schedule analysis every 6 hours
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        21600.0,  # 6 hours in seconds
        run_tweet_analysis.s(24)
    )