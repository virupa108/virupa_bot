from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.database.session import get_db
from app.models.summary import Summary
from app.models.tweet import Tweet

app = FastAPI()

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/summaries/")
def get_summaries(days: int = 30, db: Session = Depends(get_db)):
    """Get summaries for the last N days"""
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    summaries = (
        db.query(Summary)
        .filter(Summary.date_summarized >= start_date)
        .order_by(Summary.date_summarized.desc())
        .all()
    )
    return summaries


@app.get("/api/tweets/{date}")
def get_tweets_by_date(date: str, db: Session = Depends(get_db)):
    """Get tweets for a specific date"""
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
        end_date = target_date + timedelta(days=1)

        tweets = (
            db.query(Tweet)
            .filter(Tweet.created_at >= target_date)
            .filter(Tweet.created_at < end_date)
            .order_by(Tweet.created_at.desc())
            .all()
        )

        return tweets
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
