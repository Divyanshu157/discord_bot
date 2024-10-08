from celery import Celery

celery_app = Celery(
    'commands.add_to_calender.add_to_google_calendar',
    broker='redis://localhost:6379/0',  # Redis URL
    backend='redis://localhost:6379/0'
)


