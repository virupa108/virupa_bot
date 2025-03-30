from app.utils.config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.economic_calendar import EconomicCalendar
import logging
import asyncio

logger = logging.getLogger(__name__)


async def init_scheduler(db, config: Config):
    try:
        scheduler = BackgroundScheduler()
        calendar = EconomicCalendar(db, config)

        # Run immediately on startup
        await calendar.update_calendar()
        logger.info("Initial calendar update completed")

        # Schedule updates
        scheduler.add_job(
            lambda: asyncio.create_task(calendar.update_calendar()),
            "interval",
            hours=24,  # Run every 24 hours
            next_run_time=None,  # Don't run immediately again
        )

        scheduler.start()
        logger.info("Scheduler started successfully")
        return scheduler

    except Exception as e:
        logger.error(f"Error initializing scheduler: {str(e)}")
        raise
