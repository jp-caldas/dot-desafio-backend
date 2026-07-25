from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from ai_chatbot.chatbot_agent import ask_chatbot


@api_view(["POST"])
def chat(request: Request) -> Response:
    question = request.data.get("question", "")
    if not question:
        return Response({"error": "question is required"}, status=status.HTTP_400_BAD_REQUEST)
    answer = ask_chatbot(question)
    return Response({"answer": answer})