from django.apps import AppConfig

from django.db.models.signals import post_save
from .signals import my_callback


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task'

    def ready(self):
        from .models import Task
        post_save.connect(my_callback, sender=Task)
