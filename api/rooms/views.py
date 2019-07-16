from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from rooms.models import Chatroom, Message, _generate_hash
from rooms.serializers import ChatroomSerializer, MessageSerializer


class ChatroomViewSet(viewsets.ViewSet):
    """
    CRUD functionality of the Chatroom object:
        - GET
            - list, retrieve
        - POST
            - create
        - PUT
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
    def update(self, request, pk=None):
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
        serializer = ChatroomSerializer(Chatroom.objects.all())
        return Response(serializer.data)


class MessageViewSet(viewsets.ViewSet):
    """

    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
