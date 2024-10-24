from django.db import models

class Library(models.Model):
    library_name = models.CharField(max_length=255)

    def __str__(self):
        return self.library_name

class AuthorsDb(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    second_name = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'authors_db'


class BooksDb(models.Model):
    id = models.BigAutoField(primary_key=True)
    author_id = models.BigIntegerField()
    isbn = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField()
    class Meta:
        managed = False
        db_table = 'books_db'