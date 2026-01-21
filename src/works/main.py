import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()


app = Celery(
    main="scrap",
    backend="redis://redis:6379",
    broker="redis://redis:6379"
)

app.autodiscover_tasks(["src.works.tasks"])
app.conf.timezone = 'UTC'

load_dotenv()
hours = os.getenv("hours", 0)
minutes = os.getenv("minutes", 0)

app.conf.beat_schedule = {
    "make-db-backup-every-3-minutes": {
        "task": "src.works.tasks.run_scratch",
        "schedule": crontab(hour=hours, minute=minutes)
        # "schedule": crontab(minute="*/3")
    }
}
