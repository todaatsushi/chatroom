from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

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
        serializer = ChatroomSerializer(
            rooms, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        room = get_object_or_404(Chatroom, pk=pk)
        serializer = ChatroomSerializer(
            room, context={'request': request}
        )
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
        serializer = ChatroomSerializer(
            room, context={'request': request}
        )
        return Response(serializer.data)

    # DESTROY
    def destroy(self, request, pk=None):
        room = get_object_or_404(Chatroom, pk=pk)
        room.delete()

        rooms = Chatroom.objects.all()
        serializer = ChatroomSerializer(
            rooms, many=True, context={'request': request}
        )
        return Response(serializer.data)


# Api Root
@api_view(['GET'])
def root(request, format=None):
    return Response({
        'chatrooms': reverse(
            'chatroom-list', request=request, format=format
        ),
        'messages': 'http://localhost:8000/{{room_hash}}/',
    })

## MESSAGE VIEWS
@api_view(['GET', 'POST'])
def ListCreateMessages(request, hash):
    # Get relevant room
    room = get_object_or_404(Chatroom, pk=hash)

    if request.method == 'GET':
        messages = Message.objects.filter(chatroom=room)
        serializer = MessageSerializer(
            # messages, many=True, context={'request': request}
            messages, many=True, context={'request': request}
        )
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

        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def RetrieveMessage(request, id, hash):
    message = get_object_or_404(Message, pk=id)
    serializer = MessageSerializer(
        # message, context={'request': request}
        message, context={'request': request}
    )
    return Response(serializer.data)
