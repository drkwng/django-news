
def my_callback(sender, **kwargs):
    from .tasks import run_coindesk
    if kwargs.get('created'):
        instance = kwargs.get('instance')

        if instance.task_name == 'run_coindesk':
            run_coindesk.delay(instance.pk)
