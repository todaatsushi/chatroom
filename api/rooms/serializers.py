from rest_framework import serializers
from rooms.models import Chatroom, Message


class ChatroomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chatroom
        fields = [
            'hash', 'name', 'created_at', 'last_posted', 'url',
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'chatroom', 'author', 'message', 'posted_at',
        ]
