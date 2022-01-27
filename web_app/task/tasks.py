from __future__ import absolute_import, unicode_literals

from time import sleep
from celery import shared_task


@shared_task
def run_coindesk(task_pk=None):
    from news.crawlers.coindesk_crawler import run
    from .models import Task

    if task_pk:
        sleep(3)
        task = Task.objects.get(pk=task_pk)
        run(task)
    else:
        run()
