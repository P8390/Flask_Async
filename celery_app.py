from celery import Celery
from constants.common_constants import WORKER_CONFIG_MODULE

app = Celery()

app.config_from_object(WORKER_CONFIG_MODULE)
