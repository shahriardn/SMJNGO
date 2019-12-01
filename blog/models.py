from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Events(models.Model):
    title = models.CharField(max_length=100)
    short_discription = models.CharField(max_length=300, null=True)
    content = models.TextField()
    date_event = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='img/blog/events', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def tag_date_event(self):
        return f'{self.date_event}'

    tag_date_event.short_description = 'jjjj'