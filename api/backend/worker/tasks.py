from celery import Celery
from backend.configs import Configs

app = Celery("hyperion", broker=f"redis://{Configs.REDIS_HOST}")


@app.task
def add(x, y):
    return x + y
