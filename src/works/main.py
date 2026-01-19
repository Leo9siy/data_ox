import os
from datetime import timedelta

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

app.conf.beat_schedule = {
    "make-db-backup-every-night": {
        "task": "src.works.tasks.run_scratch",
        "schedule": crontab(hour=os.getenv("hours", 0), minute=os.getenv("minutes", 0))
        #"schedule": timedelta(minutes=10) #for every 5 minute
    }
}
