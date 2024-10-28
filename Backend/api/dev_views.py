from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import (
  Library, 
  AuthorsDb, 
  BooksDb,
  GenresDb,
  BookGenresDb,
  LibraryBooksDb
)

from .template_data import (
  books
)


def cleanup():
  for item in Library.objects.all():
    item.delte()

  for item in AuthorsDb.objects.all():
    item.delete()
  
  for item in BooksDb.objects.all():
    item.delete()
  
  for item in GenresDb.objects.all():
    item.delete()

  for item in BookGenresDb.objects.all():
    item.delete()

  for item in LibraryBooksDb.objects.all():
    item.delete()

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
  # cleanup()


  # Generate genres
  for genre in getGenresFromBooksRawData():
    g = GenresDb(genre=genre)
    g.save()
  
  # Generate authors
  for author in getAuthorsFromBooksRawData():
    a = AuthorsDb(first_name=author["first_name"], second_name=author["second_name"])
    a.save()

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
      publication_date=book["publication_date"]
    )
    b.save()

    # Generate book genres
    book_id = b.id
    for genre in genres:
      BookGenresDb(book=b, genre=genre).save()

  # remove all records
  # cleanup()
  return Response({
    "message": "Data saved"
  })
