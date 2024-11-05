from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/room/<str:pk>/", consumers.ChatConsumer.as_asgi()),
    path("wss/room/<str:pk>/", consumers.ChatConsumer.as_asgi())
]