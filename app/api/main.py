from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel

from app.database.session import get_db
from app.models.summary import Summary
from app.models.tweet import Tweet
from app.models.event import Event
from app.repositories import event_repository
from app.services.scheduler import init_scheduler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    init_scheduler()


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


class EventCreate(BaseModel):
    title: str
    description: str
    start: datetime
    end: datetime


@app.post("/api/events/")
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
):
    print(
        f"Creating event: {event.title}, {event.description}, {event.start}, {event.end}"
    )
    try:
        event = event_repository.create_event(
            db=db,
            title=event.title,
            description=event.description,
            start=event.start,
            end=event.end,
        )
        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update event
@app.put("/api/events/{event_id}")
def update_event(
    event_id: int,
    event: EventCreate,
    db: Session = Depends(get_db),
):
    try:
        updated_event = event_repository.update_event(
            db,
            event_id,
            title=event.title,
            description=event.description,
            start=event.start,
            end=event.end,
        )
        if not updated_event:
            raise HTTPException(status_code=404, detail="Event not found")
        return updated_event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# delete event
@app.delete("/api/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    try:
        event_repository.delete_event(db, event_id)
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# get all events
@app.get("/api/events/")
def get_events(db: Session = Depends(get_db)):
    return event_repository.get_all_events(db)
