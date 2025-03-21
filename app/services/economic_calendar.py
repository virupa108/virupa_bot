import logging
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

from app.database.session import get_db
from app.models.event import Event
from app.repositories import event_repository
from dotenv import load_dotenv
from app.utils.config import Config

logger = logging.getLogger(__name__)


class EconomicCalendar:
    def __init__(self):
        self.config = Config()

    def update_calendar(self):
        db = next(get_db())
        try:
            # Fetch events from Trading Economics
            # processed_events = self.process_events(events)

            # Add backup events for critical dates
            backup_events = self.get_critical_events()
            all_events = backup_events

            logger.info(f"All events: {all_events}")

            # Update database
            for event_data in all_events:
                try:
                    # Check if event already exists
                    existing_event = event_repository.get_event_by_title_and_date(
                        db, event_data["title"], event_data["start"]
                    )
                    # if exists and not manual then update
                    if (
                        existing_event
                        and existing_event.event_type != "manual"
                        or existing_event != "manual-economic"
                    ):
                        # Update existing event
                        event_repository.update_event(
                            db, existing_event.id, **event_data
                        )
                    else:
                        # Create new event
                        event_repository.create_event(db, **event_data)

                except Exception as e:
                    logger.error(
                        f"Error updating event {event_data['title']}: {str(e)}"
                    )
                    continue

            db.commit()

        except Exception as e:
            logger.error(f"Error in update_calendar: {str(e)}")
            db.rollback()
        finally:
            db.close()

    def get_critical_events(self) -> List[Dict[str, Any]]:
        """Get critical events from all regions"""
        critical_events = self.config.CRITICAL_EVENTS
        events = []

        for region, categories in critical_events.items():
            for category, dates in categories.items():
                for date, details in dates.items():
                    events.append(
                        {
                            "title": f"{category}-{region}",
                            "description": f"{details}",
                            "start": datetime.strptime(
                                f"{date}T14:00:00", "%Y-%m-%dT%H:%M:%S"
                            ),
                            "end": datetime.strptime(
                                f"{date}T15:00:00", "%Y-%m-%dT%H:%M:%S"
                            ),
                            "event_type": category.lower(),
                        }
                    )
        return events
