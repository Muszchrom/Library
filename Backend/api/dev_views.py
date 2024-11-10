from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
from django.db import connection

from .models import (
  Library, 
  AuthorsDb, 
  BooksDb,
  GenresDb,
  BookGenresDb,
  LibraryBooksDb
)

from .template_data import (
  books,
  libraries
)


def reset_sequences(model):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT setval(pg_get_serial_sequence('{model._meta.db_table}', 'id'), 1, false);")

def cleanup():
    Library.objects.all().delete()
    reset_sequences(Library)
    
    AuthorsDb.objects.all().delete()
    reset_sequences(AuthorsDb)
  
    BooksDb.objects.all().delete()
    reset_sequences(BooksDb)
  
    GenresDb.objects.all().delete()
    reset_sequences(GenresDb)
  
    BookGenresDb.objects.all().delete()
    reset_sequences(BookGenresDb)
  
    LibraryBooksDb.objects.all().delete()
    reset_sequences(LibraryBooksDb)

def getGenresFromBooksRawData():
  arr = []
  for book in books:
    arr += book["genres"]
  genres = list(dict.fromkeys(arr))
  return genres

def getAuthorsFromBooksRawData():
  arr = []
  for book in books:
    if book["author"] not in arr:
      arr.append(book["author"])
  return arr

@api_view(['GET'])
def generateTemplateData(request):
  # remove all records
  cleanup()


  # Generate genres
  for genre in getGenresFromBooksRawData():
    g = GenresDb(genre=genre)
    g.save()
  
  # Generate authors
  for author in getAuthorsFromBooksRawData():
    a = AuthorsDb(first_name=author["first_name"], second_name=author["second_name"])
    a.save()

  # Generate libraries
  for library in libraries:
    l = Library(
      library_name=library["library_name"],
      city=library["city"],
      latitude=library["latitude"],
      longitude=library["longitude"]
    )
    l.save()

  # Generate books 
  for book in books:
    genres = []
    for genre in book["genres"]:
      try:
        genre = GenresDb.objects.get(genre=genre)
        genres.append(genre)
      except GenresDb.DoesNotExist:
        print(f"!!!!!\tAn error occured with {genre}\t!!!!!!!!")
        continue

    b = BooksDb(
      author=AuthorsDb.objects.get(
        first_name=book["author"]["first_name"],
        second_name=book["author"]["second_name"],
      ),
      isbn=book["isbn"],
      isbn13=book["isbn13"],
      title=book["title"],
      description=book["description"],
      publication_date=book["publication_date"],
      rating = book["rating"]
    )
    b.save()

    for lib in Library.objects.all():
      if random.choice([True, False]):
        lb = LibraryBooksDb(
          library = lib,
          book = b,
          book_count = random.randint(1, 10)
        )
        lb.save()

    # Generate book genres
    book_id = b.id
    for genre in genres:
      BookGenresDb(book=b, genre=genre).save()

  # ## remove all records
  # cleanup()
  return Response({
    "message": "Data saved"
  })
