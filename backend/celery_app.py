from celery import Celery 
from celery import Celery 
from celery.schedules import crontab 

celery = Celery(
    "trekking",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    imports=["tasks"]
)

celery.conf.beat_schedule = { 
    "daily-reminder": {
        "task": "tasks.send_trek_reminder",
        "schedule": crontab(hour=9, minute=0),
    },
    "monthly-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
}