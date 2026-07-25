from django.urls import path

from ai_chatbot.views import chat

urlpatterns = [
    path("chat/", chat, name="chat"),
]