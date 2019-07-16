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
    # path('<str:pk>/<int:pk>/' ),
]

urlpatterns += router.urls
