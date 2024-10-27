from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


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

    rating = models.DecimalField(                                                               #RATING GWIAZDECZKI
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('5.0'))],
        blank=True,
        null=True  
    )

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'books_db'
        unique_together = (('isbn', 'author'),)  # Unikalna kombinacja ISBN i autora
    
    def update_rating(self, new_rating):
        if Decimal('1.0') <= new_rating <= Decimal('5.0') and (new_rating * 2) % 1 == 0:
            self.rating = new_rating
            self.save()
            return f"Ocena książki '{self.title}' została zaktualizowana na {new_rating}"
        else:
            raise ValueError("Ocena musi być liczbą od 1 do 5, z krokiem 0.5")


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


class RentalsDb(models.Model):                                         #śledzenie wypożyczeń
    user_id = models.BigIntegerField()  
    book = models.ForeignKey('BooksDb', on_delete=models.CASCADE)
    library = models.ForeignKey('Library', on_delete=models.CASCADE)
    rental_status = models.CharField(max_length=25)
    rental_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'rentals_db'