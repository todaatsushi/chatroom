from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter

import rooms.views as v


router = DefaultRouter()
router.register(
    r'chatrooms',
    v.ChatroomViewSet,
    basename='chatroom'
)

urlpatterns = [
    # Message API url endpoints
    path('messages/<str:pkr>/',
        v.ListCreateMessages,
        name='message-list'
    ), # pkr - pk of the room
]

urlpatterns += router.urls
