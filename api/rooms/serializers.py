from rest_framework import serializers
from rooms.models import Chatroom, Message


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = [
            'hash', 'name', 'created_at', 'last_posted'
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'chatroom', 'author', 'message', 'posted_at'
        ]
