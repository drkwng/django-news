from django.db import models


CHOICES = (
    ('run_coindesk', 'Run Coindesk Crawler'),
)


class Task(models.Model):
    task_name = models.CharField(max_length=255, choices=CHOICES)
    started = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.task_name

