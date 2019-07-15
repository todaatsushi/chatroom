from django.db import models
from django.utils import timezone


# Room model
class Chatroom(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_posted = models.DateTimeField(null=True)


class Message(models.Model):
    chatroom = models.ForeignKey('rooms.Chatroom', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    message = models.TextField()
