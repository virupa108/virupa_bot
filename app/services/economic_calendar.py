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
from .token_unlocks import TokenUnlocksService

logger = logging.getLogger(__name__)


class EconomicCalendar:
    def __init__(self, db, config):
        self.db = db
        self.config = config
        self.token_unlocks = TokenUnlocksService()

    async def update_calendar(self):
        try:
            # Get backup events (critical dates)
            backup_events = self.get_critical_events()
            backup_unlocks = self.get_backup_unlocks()

            # Get token unlock events
            # i dont want to keep using this api was just testing it
            # unlock_events = await self.token_unlocks.get_token_unlocks()

            # events = backup_events + unlock_events + backup_unlocks
            events = backup_events + backup_unlocks

            # Update database
            for event_data in events:
                try:
                    # Check if event already exists
                    existing_event = event_repository.get_event_by_title_and_date(
                        self.db, event_data["title"], event_data["start"]
                    )
                    # if exists and not manual then update
                    if existing_event:
                        # Update existing event
                        event_repository.update_event(
                            self.db, existing_event.id, **event_data
                        )
                    else:
                        # Create new event
                        event_repository.create_event(self.db, **event_data)

                except Exception as e:
                    logger.error(
                        f"Error updating event {event_data['title']}: {str(e)}"
                    )
                    continue

            self.db.commit()

        except Exception as e:
            logger.error(f"Error in update_calendar: {str(e)}")
            self.db.rollback()
        finally:
            self.db.close()

    def get_critical_events(self) -> List[Dict[str, Any]]:
        """Get critical events from all regions"""
        critical_events = self.config.CRITICAL_EVENTS
        events = []

        for region, categories in critical_events.items():
            for category, dates in categories.items():
                for date, details in dates.items():
                    try:
                        # Parse ISO format with UTC timezone
                        start_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
                        end_time = start_time + timedelta(hours=1)

                        events.append(
                            {
                                "title": f"{region}: {category}",
                                "description": f"{details}",
                                "start": start_time,
                                "end": end_time,
                                "event_type": category.lower(),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error parsing date {date}: {str(e)}")
                        continue

        return events

    def get_backup_unlocks(self) -> List[Dict[str, Any]]:
        """Get backup unlocks from all regions"""
        backup_unlocks = self.config.TOKEN_UNLOCKS
        return backup_unlocks
