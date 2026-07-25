from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)  # indexed for faster search
    author = models.CharField(max_length=255, db_index=True)
    publication_date = models.DateField()
    summary = models.TextField()

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"