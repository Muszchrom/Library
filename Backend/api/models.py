from django.db import models

class Library(models.Model):
    library_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if self.city:
            self.city = self.city.title()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.library_name
    class Meta:
        unique_together = ('library_name', 'city')
        db_table = 'libraries_db'



class AuthorsDb(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.first_name} {self.second_name}"
    class Meta:
        db_table = 'authors_db'


class BooksDb(models.Model):
    author = models.ForeignKey(AuthorsDb, on_delete=models.CASCADE)
    #author_id = models.BigIntegerField()
    isbn = models.CharField(max_length=10)
    isbn13 = models.CharField(max_length=13)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField()
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'books_db'
        unique_together = (('isbn', 'author'),)  # Unikalna kombinacja ISBN i autora


class GenresDb(models.Model):                                          #gatunki
    genre = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        if self.genre:
            self.genre = self.genre.title()                         # Konwersja na format Tytułowy
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.genre
    class Meta:
        db_table = 'genres_db'


class BookGenresDb(models.Model):                                      #gatunek - ksiazka (relacja wiele do wielu)
    book = models.ForeignKey('BooksDb', on_delete=models.CASCADE)
    genre = models.ForeignKey('GenresDb', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'book_genres_db'
        unique_together = (('book_id', 'genre_id'),)   


class LibraryBooksDb(models.Model):                                    #ksiazka - biblioteka
    book = models.ForeignKey('BooksDb', on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    book_count = models.IntegerField()
    class Meta:
        db_table = 'library_books_db'
        unique_together = (('book', 'library'),)                    # Zapewnia unikalność kombinacji książka-biblioteka
