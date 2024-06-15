from celery.schedules import crontab

broker_url = (
    "redis://localhost:6379/0"  # Используйте Redis в качестве брокера сообщений
)
result_backend = "redis://localhost:6379/0"
timezone = "UTC"

beat_schedule = {}
