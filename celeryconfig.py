from celery.schedules import crontab

broker_url = (
    "redis://localhost:6379/0"  # Используйте Redis в качестве брокера сообщений
)
result_backend = "redis://localhost:6379/0"
timezone = "UTC"

beat_schedule = {
    "update-database-three-times-a-day": {
        "task": "tasks.update_database",
        "schedule": crontab(
            minute="*"
        ),  # Каждый день в 8:00, 14:00 и 20:00 hour='8,14,20'
    },
}
