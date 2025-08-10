import logging
from time import time
from typing import Any

from celery import Celery
from celery.app.task import Task
from celery.signals import task_postrun, task_prerun
from core.config import CeleryConfig
from kombu.serialization import register

logger: logging.Logger = logging.getLogger(__name__)

import pydantic_serializer

# Register new serializer methods into kombu
register(
    "pydantic",
    pydantic_serializer.pydantic_dumps,
    pydantic_serializer.pydantic_loads,
    content_type="application/x-pydantic",
    content_encoding="utf-8",
)

app: Celery = Celery("ocrapp")
app.config_from_object(CeleryConfig)

app.autodiscover_tasks()

# Measure celery task execution time
# Ref: https://stackoverflow.com/questions/19481470/measuring-celery-task-execution-time
d: dict[str, float] = {}


@task_prerun.connect
def task_prerun_handler(
    signal: Any,
    sender: Any,
    task_id: str,
    task: Task,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    **extras: Any,
) -> None:
    d[task_id] = time()


@task_postrun.connect
def task_postrun_handler(
    signal: Any,
    sender: Any,
    task_id: str,
    task: Task,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    retval: Any,
    state: str,
    **extras: Any,
) -> None:
    try:
        cost = time() - d.pop(task_id)
    except KeyError:
        cost = -1

    logger.info(f"Task {task.__name__} took {cost}")
