from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'started', 'done', 'status')
    list_filter = ('started', )
    readonly_fields = ('status', 'started', 'done')


admin.site.register(Task, TaskAdmin)
