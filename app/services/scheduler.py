from apscheduler.schedulers.background import BackgroundScheduler
from app.services.economic_calendar import EconomicCalendar
import logging

logger = logging.getLogger(__name__)


def init_scheduler():
    try:
        scheduler = BackgroundScheduler()
        calendar = EconomicCalendar()

        # Run immediately on startup
        calendar.update_calendar()
        logger.info("Initial calendar update completed")

        # Then schedule periodic updates
        scheduler.add_job(
            calendar.update_calendar,
            "interval",
            hours=24,  # Run every 24 hours
            next_run_time=None,  # Don't run immediately again
        )

        scheduler.start()
        logger.info("Scheduler started successfully")
        return scheduler

    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {str(e)}")
        raise
