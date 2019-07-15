from django.db import models
from django.utils import timezone


# Room model
class Chatroom(models.Model):
    name = models.CharField(max_length=50)
    hash = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_posted = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name} - ({self.hash})'

    def get_messages(self):
        return self.messages.objects.order_by('-posted_at')

class Message(models.Model):
    chatroom = models.ForeignKey('rooms.Chatroom', on_delete=models.CASCADE, related_name='messages')
    author = models.CharField(max_length=50)
    message = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message in {self.chatroom.name}({self.chatroom.hash}) by {self.author} - {self.posted_at}'
