from datetime import datetime, timezone
import logging
from app.models.summary import Summary

logger = logging.getLogger(__name__)


def save_summary(db, summary_text: str, date_summarized: datetime):
    try:
        summary = Summary(
            summary_text=summary_text,
            created_at=datetime.now(timezone.utc),
            date_summarized=date_summarized,
        )
        db.add(summary)
        db.commit()
        return summary
    except Exception as e:
        logger.error(f"Error saving summary: {str(e)}")
        db.rollback()
        return None


def get_summary_by_date(db, date: datetime):
    """Get summary for a specific date"""
    return db.query(Summary).filter(Summary.date_summarized == date).first()
