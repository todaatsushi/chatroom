from django.contrib import admin
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

import rooms.views as v


# schema_view = get_schema_view(title="Chatroom API")

router = DefaultRouter()
router.register(
    r'chatrooms',
    v.ChatroomViewSet,
    basename='chatroom'
)

urlpatterns = [
    path('', v.root, name='chatroom-root'),
    # Message API url endpoints
    path('messages/<str:hash>/', v.ListCreateMessages,
        name='message-list'), # pkr - pk of the room
    path('messages/<str:hash>/<int:id>/', v.RetrieveMessage, name='message-detail'),
]

urlpatterns += router.urls
