from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.event import Event
from datetime import datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def create_event(
    db: Session, title: str, description: str, start: datetime, end: datetime
) -> Event:
    try:
        event = Event(
            title=title,
            description=description,
            start=start,
            end=end,
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
    return db.query(Event).order_by(Event.start.desc()).all()


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
