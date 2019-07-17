from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rooms.models import Chatroom, Message, _generate_hash
from rooms.serializers import ChatroomSerializer, MessageSerializer


class ChatroomViewSet(viewsets.ViewSet):
    """
    CRUD functionality of the Chatroom object:
        - GET
            - list, retrieve
        - POST
            - create
        - PATCH
            - update, partial_update
        - DESTROY
            - destroy
    """

    # GET
    def list(self, request):
        rooms = Chatroom.objects.all()
        serializer = ChatroomSerializer(rooms, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        room = get_object_or_404(Chatroom, pk=pk)
        serializer = ChatroomSerializer(room)
        return Response(serializer.data)

    # POST
    def create(self, request):
        name = request.data['name']
        room = Chatroom(
            name=name
        )
        room.save()
        return Response(
            room.as_dict()
        )

    # PUT / PATCH
    def partial_update(self, request, pk=None):
        room = get_object_or_404(Chatroom, pk=pk)

        if 'name' in request.data:
            room.name = request.data['name']
        
        if 'last_posted' in request.data:
            room.last_posted = request.data['last_posted']

        room.save()
        serializer = ChatroomSerializer(room)
        return Response(serializer.data)

    # DESTROY
    def destroy(self, request, pk=None):
        room = get_object_or_404(Chatroom, pk=pk)
        room.delete()

        rooms = Chatroom.objects.all()
        serializer = ChatroomSerializer(rooms, many=True)
        return Response(serializer.data)


## MESSAGE VIEWS
@api_view(['GET', 'POST'])
def ListCreateMessages(request, pkr):
    # Get relevant room
    room = get_object_or_404(Chatroom, pk=pkr)

    if request.method == 'GET':
        messages = Message.objects.filter(chatroom=room)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        author = request.data['author']
        message = request.data['message']
        message = Message(
            chatroom=room,
            author=author,
            message=message
        )

        message.save()

        # Update last_posted at on room
        room.last_posted = timezone.now()
        room.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data)

@api_view(['GET'])
def RetrieveMessage(request, pk, pkr):
    # Get relevant room
    room = get_object_or_404(Chatroom, pk=pkr)
    message = get_object_or_404(Message, pk=pk)
    serializer = MessageSerializer(message)
    return Response(serializer.data)

