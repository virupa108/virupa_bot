from typing import List, Dict
from datetime import datetime, timedelta

class AnalysisQueries:
    def __init__(self, db_session):
        self.db = db_session

    def get_latest_analysis(self) -> TweetBatchAnalysis:
        return self.db.query(TweetBatchAnalysis)\
            .order_by(TweetBatchAnalysis.timestamp.desc())\
            .first()

    def get_trending_topics_over_time(self, days: int = 7) -> List[Dict]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        analyses = self.db.query(TweetBatchAnalysis)\
            .filter(TweetBatchAnalysis.timestamp >= cutoff)\
            .order_by(TweetBatchAnalysis.timestamp)\
            .all()

        return [{
            'timestamp': analysis.timestamp,
            'topics': analysis.main_topics,
            'sentiment': analysis.sentiment_summary
        } for analysis in analyses]

    def get_sentiment_trends(self, days: int = 7) -> Dict:
        analyses = self.get_trending_topics_over_time(days)

        sentiment_trends = {
            'positive': [],
            'negative': [],
            'neutral': []
        }

        for analysis in analyses:
            if 'breakdown' in analysis['sentiment']:
                for sentiment_type in sentiment_trends.keys():
                    sentiment_trends[sentiment_type].append({
                        'timestamp': analysis['timestamp'],
                        'value': analysis['sentiment']['breakdown'][sentiment_type]
                    })

        return sentiment_trends