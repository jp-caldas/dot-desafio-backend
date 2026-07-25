from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from semantic_search.embeddings_store import search as semantic_search


@api_view(["POST"])
def search(request: Request) -> Response:
    query = request.data.get("query", "")
    if not query:
        return Response({"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST)
    results = semantic_search(query, k=2)
    return Response({"results": results})