from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.event import Event
from datetime import datetime
from typing import List, Optional
import logging
from sqlalchemy import or_

logger = logging.getLogger(__name__)


def create_event(
    db: Session,
    title: str,
    description: str,
    start: datetime,
    end: datetime,
    event_type: str = "manual",
) -> Event:
    try:
        event = Event(
            title=title,
            description=description,
            start=start,
            end=end,
            event_type=event_type,
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    except IntegrityError:
        db.rollback()
        raise


def get_event_by_id(db: Session, event_id: int) -> Optional[Event]:
    return db.query(Event).filter(Event.id == event_id).first()


def get_all_events(db: Session) -> List[Event]:
    vesting_event_to_filter = ["celestia", "sei"]

    # Create filter conditions for each token
    token_filters = [
        Event.description.ilike(f"%{token}%") for token in vesting_event_to_filter
    ]

    return (
        db.query(Event)
        .filter(~((Event.event_type == "vesting") & or_(*token_filters)))
        .order_by(Event.start.desc())
        .all()
    )


def update_event(db: Session, event_id: int, **kwargs) -> Optional[Event]:
    event = get_event_by_id(db, event_id)
    if event:
        for key, value in kwargs.items():
            setattr(event, key, value)
        db.commit()
        db.refresh(event)
    return event


def delete_event(db: Session, event_id: int) -> bool:
    event = get_event_by_id(db, event_id)
    if event:
        db.delete(event)
        db.commit()
        return True
    return False


def get_events_by_date_range(
    db: Session, start: datetime, end: datetime
) -> List[Event]:
    return (
        db.query(Event)
        .filter(Event.start >= start)
        .filter(Event.end <= end)
        .order_by(Event.start.desc())
        .all()
    )


def save_event(db: Session, event_data: dict) -> Optional[Event]:
    try:
        event = Event(**event_data)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event
    except Exception as e:
        logger.error(f"Error saving event: {str(e)}")
        db.rollback()
        return None


def get_event_by_title_and_date(db: Session, title: str, start_date: datetime) -> Event:
    return (
        db.query(Event).filter(Event.title == title, Event.start == start_date).first()
    )
