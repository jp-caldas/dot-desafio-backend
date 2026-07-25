import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from library.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def book_data():
    return {
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "publication_date": "2003-08-30",
        "summary": "A comprehensive guide to domain-driven design principles.",
    }


@pytest.mark.django_db
class TestBookAPI:
    def test_create_book(self, api_client, book_data):
        response = api_client.post(reverse("book-list"), book_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == book_data["title"]
        assert "id" in response.data

    def test_list_books(self, api_client, book_data):
        api_client.post(reverse("book-list"), book_data, format="json")
        response = api_client.get(reverse("book-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_filter_by_title(self, api_client):
        Book.objects.create(title="Design Patterns", author="Gang of Four",
                            publication_date="1994-10-21", summary="Elements of reusable OO software.")
        Book.objects.create(title="Clean Architecture", author="Robert C. Martin",
                            publication_date="2017-09-20", summary="A craftsman's guide to software structure.")
        response = api_client.get(reverse("book-list"), {"title__icontains": "clean"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Clean Architecture"

    def test_filter_by_author(self, api_client):
        Book.objects.create(title="Refactoring", author="Martin Fowler",
                            publication_date="1999-07-08", summary="Improving the design of existing code.")
        response = api_client.get(reverse("book-list"), {"author__icontains": "fowler"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_get_book_not_found(self, api_client):
        response = api_client.get(reverse("book-detail", kwargs={"pk": 999}))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_book(self, api_client, book_data):
        create_resp = api_client.post(reverse("book-list"), book_data, format="json")
        book_id = create_resp.data["id"]
        updated = {**book_data, "title": "Test Updated"}
        response = api_client.put(reverse("book-detail", kwargs={"pk": book_id}), updated, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Test Updated"

    def test_delete_book(self, api_client, book_data):
        create_resp = api_client.post(reverse("book-list"), book_data, format="json")
        book_id = create_resp.data["id"]
        response = api_client.delete(reverse("book-detail", kwargs={"pk": book_id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == 0