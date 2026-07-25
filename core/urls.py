from django.urls import include, path

urlpatterns = [
    path("api/", include("library.urls")),
    path("api/", include("ai_chatbot.urls")),
    path("api/", include("semantic_search.urls")),
]