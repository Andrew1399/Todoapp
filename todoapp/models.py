import datetime
from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=True, null=True)
    desired_time = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ('completed', )

    def count_uncompleted_tasks(self):
        return self.completed.all().count()

    def count_time_completing(self):
        return (self.updated_at - self.date_added).days

    def count_time_in_process(self):
        return (datetime.date.today() - self.date_added.date()).days

    def __str__(self):
        return self.title

