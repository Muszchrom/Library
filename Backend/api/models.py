from django.db import models

class Library(models.Model):
    library_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if self.city:
            self.city = self.city.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.library_name
        
    class Meta:
        db_table = 'libraries_db'

class AuthorsDb(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.first_name} {self.second_name}"
    class Meta:
        db_table = 'authors_db'

class BooksDb(models.Model):
    author_id = models.BigIntegerField()
    isbn = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField()
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'books_db'