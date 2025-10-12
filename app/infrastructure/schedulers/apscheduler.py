from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.domain.ports.scheduler import IScheduler


class APSchedulerService(IScheduler):
    def __init__(self):
        self._scheduler = AsyncIOScheduler()

    async def start(self):
        self._scheduler.start()

    async def stop(self):
        self._scheduler.shutdown()

    async def schedule_interval(self, name: str, interval_seconds: int, task):
        self._scheduler.add_job(
            task, IntervalTrigger(seconds=interval_seconds), id=name
        )

    async def cancel(self, name: str):
        self._scheduler.remove_job(name)
