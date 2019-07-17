from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

import rooms.views as v


schema_view = get_schema_view(title="Chatroom API")

router = DefaultRouter()
router.register(
    r'chatrooms',
    v.ChatroomViewSet,
    basename='chatroom'
)

urlpatterns = [
    path('', schema_view, name='chatroom-schema'),
    # Message API url endpoints
    path('messages/<str:pkr>/',
        v.ListCreateMessages,
        name='message-list'
    ), # pkr - pk of the room
]

urlpatterns += router.urls
