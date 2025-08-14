from __future__ import annotations

import time
from datetime import datetime
from croniter import croniter

from app.core.config import settings
from app.jobs import queue, tasks_analytics, tasks_notifications


def schedule_loop() -> None:
    next_analytics = croniter(
        settings.ANALYTICS_REFRESH_CRON, datetime.utcnow()
    ).get_next(datetime)
    next_cleanup = croniter(
        settings.NOTIFICATIONS_CLEANUP_CRON, datetime.utcnow()
    ).get_next(datetime)
    while True:  # pragma: no cover - long running process
        now = datetime.utcnow()
        if now >= next_analytics:
            queue.enqueue(
                "analytics.refresh", tasks_analytics.rebuild_analytics_cache, "global"
            )
            next_analytics = croniter(settings.ANALYTICS_REFRESH_CRON, now).get_next(
                datetime
            )
        if now >= next_cleanup:
            queue.enqueue(
                "notifications.cleanup", tasks_notifications.cleanup_notifications
            )
            next_cleanup = croniter(settings.NOTIFICATIONS_CLEANUP_CRON, now).get_next(
                datetime
            )
        time.sleep(30)


if __name__ == "__main__":  # pragma: no cover
    schedule_loop()
