from celery import Celery

app = Celery("dj_project", include=["dj_project.tasks"])
app.conf.broker_url = "redis://localhost:6379"
app.conf.result_backend = "redis://localhost:6379"
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Oslo",
    enable_utc=True,
)