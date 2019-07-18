from django.db import models
from django.utils import timezone


def _generate_hash():
    import uuid
    return str(uuid.uuid4().hex)[:10]


class Chatroom(models.Model):
    hash = models.CharField(
        primary_key=True,
        default=_generate_hash,
        editable=False,
        max_length=10,
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    last_posted = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.name} - ({self.hash})'

    def get_messages(self):
        return self.messages.order_by('-posted_at')

    def as_dict(self):
        return {
            'hash': self.hash,
            'name': self.name,
            'created_at': self.created_at,
            'last_posted': self.last_posted,
        }


class Message(models.Model):
    chatroom = models.ForeignKey(
        'rooms.Chatroom',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    author = models.CharField(max_length=50)
    message = models.TextField()
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message in {self.chatroom.name}({self.chatroom.hash}) by {self.author} - {self.posted_at}'

    def as_dict(self):
        return {
            'id': self.pk,
            'chatroom': self.chatroom,
            'author': self.author,
            'message': self.message,
            'posted_at': self.posted_at,
        }
