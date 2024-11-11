from rest_framework import viewsets
from rest_framework import status

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from geopy.distance import geodesic
from django.shortcuts import get_object_or_404
from django.core.files import File
from django.conf import settings


from .models import (
    Library, 
    AuthorsDb, 
    BooksDb,
    GenresDb,
    BookGenresDb,
    LibraryBooksDb,
    RentalsDb
)

from .serializers import (
    LibrarySerializer, 
    AuthorsDbSerializer, 
    BooksDbSerializer,
    GenresDbSerializer,
    BookGenresDbSerializer,
    LibraryBooksDbSerializer,
    RentalsDbSerializer
)

'''             OBSŁUGA BIBLIOTEK            '''
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    def get_queryset(self):
        queryset = super().get_queryset()                                       
        city = self.request.query_params.get('city', None)                      
        if city is not None:
            city = city.title()
            queryset = queryset.filter(city__iexact=city)                      
            if not queryset.exists():  
                raise NotFound(detail=f"No libraries found in {city}.")      
        return queryset

    def create(self, request, *args, **kwargs):
        city = request.data.get('city', '').strip()
        library_name = request.data.get('library_name', '').strip()
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)

        #sprawdzanie pustych pól
        if not city:
            raise ValidationError("City is required.")
        if not library_name:
            raise ValidationError("Library name is required.")
        if not latitude or not longitude:
            raise ValidationError("Latitude and longitude are required.")

        #sprawdzamy czy biblioteka już istnieje przy tworzeniu
        if Library.objects.filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city = request.data.get('city', instance.city).title()
        library_name = request.data.get('library_name', instance.library_name)
        lalitude = request.data.get('latitude', instance.latitude)
        longitude = request.data.get('longitude', instance.longitude)

        if not library_name:
            raise ValidationError("Library name is required.")

        if not city:
            raise ValidationError("City is required.")
        if not latitude or not longitude:
            raise ValidationError("Latitude and longitude are required.")

        if Library.objects.exclude(id=instance.id).filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        return super().update(request, *args, **kwargs)
         
    def retrieve(self, request, *args, **kwargs):
        identifier = kwargs.get('pk')
        if identifier is None:
            raise NotFound(detail="Library identifier is required. ")                 # nazwa lub di
        try:
            if identifier.isdigit():                                                  #jako id
                instance = Library.objects.get(id=int(identifier))
            else:  
                instance = Library.objects.get(library_name__iexact=identifier)       #jako nazwa
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Library.DoesNotExist:
            raise NotFound(detail="Library NOT found.")



'''             OBSŁUGA AUTORÓW            '''
class AuthorsDbViewSet(viewsets.ModelViewSet):
    queryset = AuthorsDb.objects.all()
    serializer_class = AuthorsDbSerializer
    def create(self, request, *args, **kwargs):
            first_name = request.data.get('first_name')                                 #pobieranie imie i nazwisko
            second_name = request.data.get('second_name')

            formatted_first_name = first_name.title() if first_name else None           # .title()
            formatted_second_name = second_name.title() if second_name else None

            existing_author = AuthorsDb.objects.filter(                                 # spradzanie filtrowanie czy istnieje juz
                first_name__iexact=formatted_first_name,
                second_name__iexact=formatted_second_name
            ).first()

            if existing_author:                                                         #jesli istnieje zwraca id imie nazwisko
                return Response({
                    'message': f'Autor {existing_author.first_name} {existing_author.second_name} już istnieje.',           #TO POLE DO TESTOWANIA, MOŻNA USUNAC
                    'id': existing_author.id,
                    'first_name': existing_author.first_name,
                    'second_name': existing_author.second_name
                }, status=200)

            author_data = {                                                            # Jeśli autor nie istnieje, tworzy nwoego
                'first_name': formatted_first_name,
                'second_name': formatted_second_name
            }

            serializer = self.get_serializer(data=author_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)



'''             OBSŁUGA KSIĄŻEK            '''
class BooksDbViewSet(viewsets.ModelViewSet):
    queryset = BooksDb.objects.all()
    serializer_class = BooksDbSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        author_id = data.get('author')

        if author_id:
            try:
                author = AuthorsDb.objects.get(id=author_id)
                data['author'] = author.id
            except AuthorsDb.DoesNotExist:
                return Response({"error": "Author does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Author is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            book = serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser], url_path='upload-cover')
    def upload_cover(self, request, pk=None):
        book = self.get_object() 
        if 'cover_book' not in request.FILES:
            return Response({"error": "No cover image provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        cover_book = request.FILES['cover_book']
        book.cover_book.save(cover_book.name, cover_book, save=True)

        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''             OBSŁUGA GATUNKÓW KSIĄŻEK            '''
class GenreDbViewSet(viewsets.ModelViewSet):
    queryset = GenresDb.objects.all()
    serializer_class = GenresDbSerializer

    def create(self, request, *args, **kwargs):
        genre_name = request.data.get('genre', '').title()
        existing_genre = GenresDb.objects.filter(genre__iexact=genre_name).first()
        
        if existing_genre:
            return Response({
                'message': f"Genre '{existing_genre.genre}' already exists.",
                'id': existing_genre.id,
                'genre': existing_genre.genre
            }, status=status.HTTP_200_OK)

        # Użycie serializer z walidacją
        serializer = self.get_serializer(data={'genre': genre_name})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        lookup_value = kwargs.get('pk')

        if lookup_value == "all":
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        if lookup_value.isdigit():
            return super().retrieve(request, *args, **kwargs)  # ID-based retrieval
        try:
            genre = GenresDb.objects.get(genre__iexact=lookup_value.title())  # Name-based retrieval
            serializer = self.get_serializer(genre)
            return Response(serializer.data)
        except GenresDb.DoesNotExist:
            raise NotFound(detail=f"Genre '{lookup_value}' does not exist.")


'''             RELACJA KSIĄŻKA GATUNEK            '''
class BookGenresDbViewSet(viewsets.ModelViewSet):
    queryset = BookGenresDb.objects.all()
    serializer_class = BookGenresDbSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        genre_id = request.data.get('genre')

        if not book_id or not genre_id:
            return Response({"error": "Both book and genre are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            book = BooksDb.objects.get(id=book_id)
            genre = GenresDb.objects.get(id=genre_id)

            if BookGenresDb.objects.filter(book=book, genre=genre).exists():
                return Response({"error": "This book-genre relation already exists."}, status=status.HTTP_400_BAD_REQUEST)

            book_genre = BookGenresDb(book=book, genre=genre)
            book_genre.save()

            return Response({"book": book_id, "genre": genre_id}, status=status.HTTP_201_CREATED)

        except BooksDb.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except GenresDb.DoesNotExist:
            return Response({"error": "Genre does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            book_genre = self.get_object()
            book_genre.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BookGenresDb.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


'''             RELACJA BIBLIOTEKA KSIĄŻKA            '''
class LibraryBooksDbViewSet(viewsets.ModelViewSet):
    queryset = LibraryBooksDb.objects.all()
    serializer_class = LibraryBooksDbSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        library_id = request.data.get('library')
        book_count = request.data.get('book_count')
        # Sprawdzamy, czy book_count jest podane i jest liczbą dodatnią
        if book_count is None or int(book_count) < 0:
            return Response({"error": "Book count must be a non-negative integer."}, status=status.HTTP_400_BAD_REQUEST)
        if not book_id or not library_id:
            return Response({"error": "Both book and library are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = BooksDb.objects.get(id=book_id)
            library = Library.objects.get(id=library_id)
            # Sprawdzenie, czy relacja już istnieje
            if LibraryBooksDb.objects.filter(book=book, library=library).exists():
                return Response({"error": "This book-library relation already exists."}, status=status.HTTP_400_BAD_REQUEST)
            # Tworzenie nowej relacji
            library_book = LibraryBooksDb(book=book, library=library, book_count=book_count)
            library_book.save()
            return Response({"book": book_id, "library": library_id, "book_count": book_count}, status=status.HTTP_201_CREATED)
        except BooksDb.DoesNotExist:
            return Response({"error": "Book does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Library.DoesNotExist:
            return Response({"error": "Library does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "A database integrity error occurred."}, status=status.HTTP_400_BAD_REQUEST)
            
    def update(self, request, pk=None):
        try:
            library_book = self.get_object()  # Pobieranie obiektu na podstawie PK
            book_count = request.data.get('book_count')
            # Sprawdzenie, czy book_count jest podane i jest liczbą dodatnią lub zerową
            if book_count is not None:
                if int(book_count) < 0:
                    return Response({"error": "Book count must be a non-negative integer."}, status=status.HTTP_400_BAD_REQUEST)
                # Aktualizacja book_count
                library_book.book_count = book_count 
            library_book.save()  # Zapisanie zmienionego obiektu
            return Response({"book": library_book.book.id, "library": library_book.library.id, "book_count": library_book.book_count}, status=status.HTTP_200_OK)
        except LibraryBooksDb.DoesNotExist:
            return Response({"error": "Library book relation does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({"error": "A database integrity error occurred."}, status=status.HTTP_400_BAD_REQUEST)
        

'''                BESTSELLERY            '''
class BestSellerBooksViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BooksDb.objects.order_by('-rating')[:15]
    serializer_class = BooksDbSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

'''             OBSŁUGA WYPOŻYCZEŃ            '''
class RentalsDbViewSet(viewsets.ModelViewSet):
    queryset = RentalsDb.objects.all()
    serializer_class = RentalsDbSerializer

#               OBSŁUGA BEST-NEAREST
class BestNearestView(APIView):
    def get(self, request):
        default_location = (51.246452, 22.568446)  # default location if user doesnt allow location access
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude and longitude:
            try:
                user_location = (float(latitude), float(longitude))
            except ValueError:
                return Response({"message": "Invalid coordinates"}, status=400)
        else:
            user_location = default_location

        libraries = Library.objects.all()
        if not libraries:
            return Response({"message": "No libraries found"}, status=404)

        
        libraries_with_distance = [
            (library, geodesic(user_location, (library.latitude, library.longitude)).kilometers)
            for library in libraries
        ]
       
        nearest_libraries = sorted(libraries_with_distance, key=lambda x: x[1])[:5]
    
        books = []
        book_ids = set()
        for library, distance in nearest_libraries:
            library_books = LibraryBooksDb.objects.filter(library=library).select_related('book').order_by('-book__rating')
            for library_book in library_books:
                if library_book.book.id not in book_ids:
                    books.append(library_book.book)
                    book_ids.add(library_book.book.id)
                if len(books) == 25:
                    break
            if len(books) == 25:
                break

        
        books = sorted(books, key=lambda book: book.rating, reverse=True)

        serializer = BooksDbSerializer(books, many=True)
        return Response(serializer.data)


class BooksByGenreView(APIView):
    def get(self, request, genre_id):
        books = BooksDb.objects.filter(bookgenresdb__genre_id=genre_id).distinct()
        serializer = BooksDbSerializer(books, many=True)
        return Response(serializer.data)
    
class LibraryBooksByGenreView(APIView):
    def get(self, request, library_id, genre_id):
        try:
            library = Library.objects.get(id=library_id)
        except Library.DoesNotExist:
            raise NotFound(detail="Library not found.")

        books = BooksDb.objects.filter(
            librarybooksdb__library=library,
            bookgenresdb__genre_id=genre_id
        ).distinct()

        serializer = BooksDbSerializer(books, many=True)
        return Response(serializer.data)