from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    # icontains allows partial matching (e.g. "rama" matches "Ramalho")
    filterset_fields = {
        "title": ["icontains"],
        "author": ["icontains"],
    }