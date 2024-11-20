from rest_framework import viewsets
from rest_framework import status

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from geopy.distance import geodesic
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.core.files import File
from django.conf import settings
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from django.db import transaction


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
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        book_id = self.request.query_params.get('book', None)

        if city:
            city = city.title()
            queryset = queryset.filter(city__iexact=city)
            if not queryset.exists():
                raise NotFound(detail=f"No libraries found in {city}.")

        if latitude and longitude:
            try:
                user_location = (float(latitude), float(longitude))
            except ValueError:
                raise ValidationError("Invalid coordinates.")

            if book_id:
                queryset = queryset.filter(librarybooksdb__book_id=book_id)
                if not queryset.exists():
                    raise NotFound(detail="No libraries found with the specified book.")

            libraries_with_distance = [
                {
                    'id': library.id,
                    'library_name': library.library_name,
                    'city': library.city,
                    'distance': round(geodesic(user_location, (library.latitude, library.longitude)).kilometers, 2)
                }
                for library in queryset
            ]
            
            sorted_libraries = sorted(libraries_with_distance, key=lambda x: x['distance'])
            return sorted_libraries

        return queryset

    def list(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        if latitude and longitude:
            libraries_with_distance = self.get_queryset()
            return Response(libraries_with_distance)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        city = request.data.get('city', '').strip()
        library_name = request.data.get('library_name', '').strip()
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)

        if not city:
            raise ValidationError("City is required.")
        if not library_name:
            raise ValidationError("Library name is required.")
        if not latitude or not longitude:
            raise ValidationError("Latitude and longitude are required.")

        if Library.objects.filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city = request.data.get('city', instance.city).title()
        library_name = request.data.get('library_name', instance.library_name)
        latitude = request.data.get('latitude', instance.latitude)
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
            raise NotFound(detail="Library identifier is required.")  
        try:
            if identifier.isdigit():
                instance = Library.objects.get(id=int(identifier))
            else:
                instance = Library.objects.get(library_name__iexact=identifier)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        
        genre_name = self.request.query_params.get('genre', None)
        if genre_name:
            queryset = queryset.filter(bookgenresdb__genre__genre__iexact=genre_name)

        author_param = self.request.query_params.get('author', None)
        if author_param:
            if author_param.isdigit():
                queryset = queryset.filter(author_id=int(author_param))
            else:
                try:
                    first_name, second_name = author_param.split()
                    queryset = queryset.filter(
                        author__first_name__iexact=first_name,
                        author__second_name__iexact=second_name
                    )
                except ValueError:
                    raise serializers.ValidationError("Author parameter should be in 'First Last' format.")

        rating = self.request.query_params.get('rating', None)
        if rating:
            try:
                rating = float(rating)
                queryset = queryset.filter(rating=rating)
            except ValueError:
                raise serializers.ValidationError("Rating must be a valid number.")

        title_param = self.request.query_params.get('title', None)
        if title_param:
            all_titles = list(BooksDb.objects.values_list('title', flat=True))
            matching_titles = [
                title for title in all_titles
                if fuzz.partial_ratio(title_param.lower(), title.lower()) >= 80
            ]

            if matching_titles:
                queryset = queryset.filter(title__in=matching_titles)
            else:
                raise ValidationError(f"No matching titles found for '{title_param}'.")

        search_param = self.request.query_params.get('search', None)
        if search_param:
            search_param = search_param.lower()
            all_books = BooksDb.objects.select_related('author').all()
            matching_books = []

            for book in all_books:
                author_full_name = f"{book.author.first_name.lower()} {book.author.second_name.lower()}"
                author_reversed_name = f"{book.author.second_name.lower()} {book.author.first_name.lower()}"
                
                if (
                    fuzz.partial_ratio(search_param, book.title.lower()) >= 70 or
                    fuzz.partial_ratio(search_param, author_full_name) >= 70 or
                    fuzz.partial_ratio(search_param, author_reversed_name) >= 70
                ):
                    matching_books.append(book.id)

            if matching_books:
                queryset = queryset.filter(id__in=matching_books)
            else:
                raise ValidationError(f"No matches found for '{search_param}'.")

        return queryset

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
    def upload_cover(self, request):
        book = self.get_object() 
        if 'cover_book' not in request.FILES:
            return Response({"error": "No cover image provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        cover_book = request.FILES['cover_book']
        book.cover_book.save(cover_book.name, cover_book, save=True)

        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='library/(?P<library_id>[^/.]+)/rent')
    @transaction.atomic

    # POST /books/{id}/library/{library_id}/rent/ - Rent a book from a library.
    def rent_from_library(self, request, pk=None, library_id=None):
        try:
            book = BooksDb.objects.get(pk=pk)
            library = Library.objects.get(pk=library_id)
        except BooksDb.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Library.DoesNotExist:
            return Response({"error": "Library not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check the book availability in the library
        try:
            library_book = LibraryBooksDb.objects.get(book=book, library=library)
            if library_book.book_count <= 0:
                return Response({"error": "No copies of this book are available in the selected library."}, status=status.HTTP_400_BAD_REQUEST)
        except LibraryBooksDb.DoesNotExist:
            return Response({"error": "This book is not available in the selected library."}, status=status.HTTP_404_NOT_FOUND)

        # Parse user role and ID from headers
        x_role_id = request.META.get('HTTP_X_ROLE_ID')
        if not x_role_id:
            return Response({"error": "User role and ID not provided in the headers."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            role, user_id = x_role_id.split()
            role = int(role)
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid format for X-role-id header."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rented 2 active copies of this book from the library
        active_rentals = RentalsDb.objects.filter(
            user_id=user_id,
            book=book,
            library=library,
            return_date__isnull=True
        )
        if active_rentals.count() >= 2:
            return Response({"error": "You cannot rent more than 2 active copies of the same book from this library."}, status=status.HTTP_400_BAD_REQUEST)

        # Process the rental
        rental_status = "Rented"
        rental_date = date.today()
        due_date = rental_date + timedelta(days=14)

        # Create a rental record
        RentalsDb.objects.create(
            user_id=user_id,
            book=book,
            library=library,
            rental_status=rental_status,
            rental_date=rental_date,
            due_date=due_date
        )

        # Update the library's book count
        library_book.book_count -= 1
        library_book.save()

        return Response({
            "message": f"Book '{book.title}' successfully rented from '{library.library_name}'.",
            "rental_status": rental_status,
            "rental_date": rental_date,
            "due_date": due_date
        }, status=status.HTTP_201_CREATED)

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

        serializer = self.get_serializer(data={'genre': genre_name})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        genre_id = request.query_params.get('id', None)
        genre_name = request.query_params.get('genre', None)

        if genre_id:
            try:
                genre = GenresDb.objects.get(id=genre_id)
                books = BooksDb.objects.filter(bookgenresdb__genre=genre).distinct()
                books_serializer = BooksDbSerializer(books, many=True)
                return Response(books_serializer.data)
            except GenresDb.DoesNotExist:
                raise NotFound(detail=f"Genre with id '{genre_id}' does not exist.")
        
        if genre_name:
            genre_name = genre_name.title()
            try:
                genre = GenresDb.objects.get(genre__iexact=genre_name)
                books = BooksDb.objects.filter(bookgenresdb__genre=genre).distinct()
                books_serializer = BooksDbSerializer(books, many=True)
                return Response(books_serializer.data)
            except GenresDb.DoesNotExist:
                raise NotFound(detail=f"Genre '{genre_name}' does not exist.")
        
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
            return super().retrieve(request, *args, **kwargs)  
        try:
            genre = GenresDb.objects.get(genre__iexact=lookup_value.title())
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

'''               OBSŁUGA BEST-NEAREST          '''
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

    
# class TestHeaderView(APIView):
#     def get(self, request, *args, **kwargs):
#         x_role_id = request.META.get('HTTP_X_ROLE_ID', None)
#         return Response({
#             "X-role-id": x_role_id,
#         })
'''             OBSŁUGA WYPOŻYCZEŃ            '''
class RentalsDbViewSet(viewsets.ViewSet):
    queryset = RentalsDb.objects.all()
    serializer_class = RentalsDbSerializer

    def list(self, request, *args, **kwargs):
        """
        GET /rental/ - Retrieve all rentals.
        """
        rentals = self.queryset
        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        GET /rental/{id}/ - Retrieve a specific rental by ID.
        """
        try:
            rental = RentalsDb.objects.get(pk=pk)
            serializer = self.serializer_class(rental)
            return Response(serializer.data)
        except RentalsDb.DoesNotExist:
            raise NotFound(detail="Rental not found.")

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def rentals_by_user(self, request, user_id=None):
        """
        GET /rental/user/{user_id}/ - Retrieve rentals for a specific user.
        """
        rentals = RentalsDb.objects.filter(user_id=user_id)
        if not rentals.exists():
            return Response({"error": f"No rentals found for user with ID {user_id}."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(rentals, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        POST /rental/ - Rent a book.
        """
        book_id = request.data.get('book_id')
        library_id = request.data.get('library_id')

        if not book_id or not library_id:
            return Response({"error": "Both 'book_id' and 'library_id' are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = BooksDb.objects.get(pk=book_id)
            library = Library.objects.get(pk=library_id)
        except BooksDb.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Library.DoesNotExist:
            return Response({"error": "Library not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check availability in the library
        try:
            library_book = LibraryBooksDb.objects.get(book=book, library=library)
            if library_book.book_count <= 0:
                return Response({"error": "No copies of this book are available in the selected library."}, status=status.HTTP_400_BAD_REQUEST)
        except LibraryBooksDb.DoesNotExist:
            return Response({"error": "This book is not available in the selected library."}, status=status.HTTP_404_NOT_FOUND)

        # Get user role and ID from the header
        x_role_id = request.META.get('HTTP_X_ROLE_ID')  # Default value for testing
        try:
            role, user_id = x_role_id.split()
            role = int(role)
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid format for X-role-id header."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already rented 2 active copies of this book from the library
        active_rentals = RentalsDb.objects.filter(
            user_id=user_id,
            book=book,
            library=library,
            return_date__isnull=True
        )
        if active_rentals.count() >= 2:
            return Response({"error": "You cannot rent more than 2 active copies of the same book from this library."}, status=status.HTTP_400_BAD_REQUEST)

        rental_status = "Rented"
        rental_date = date.today()
        due_date = rental_date + timedelta(days=14)  # Example: 2-week rental period

        RentalsDb.objects.create(
            user_id=user_id,
            book=book,
            library=library,
            rental_status=rental_status,
            rental_date=rental_date,
            due_date=due_date
        )

        library_book.book_count -= 1
        library_book.save()

        return Response({
            "message": f"Book '{book.title}' successfully rented from '{library.library_name}'.",
            "rental_status": rental_status,
            "rental_date": rental_date,
            "due_date": due_date
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        """
        PUT /rental/{id}/ - Return a rented book.
        """
        try:
            rental = RentalsDb.objects.get(pk=pk, return_date__isnull=True)
        except RentalsDb.DoesNotExist:
            return Response({"error": "Active rental not found."}, status=status.HTTP_404_NOT_FOUND)

        rental.return_date = date.today()
        rental.rental_status = "Returned"
        rental.save()

        library_book = LibraryBooksDb.objects.get(book=rental.book, library=rental.library)
        library_book.book_count += 1
        library_book.save()

        return Response({"message": "Book successfully returned.", "rental_id": rental.id}, status=status.HTTP_200_OK)