from rest_framework import viewsets
from rest_framework import status

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError


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
<<<<<<< HEAD
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)
=======
>>>>>>> fe008d114886a306d62feb191f3a0f6d32a4e575

        #sprawdzanie pustych pól
        if not city:
            raise ValidationError("City is required.")
        if not library_name:
            raise ValidationError("Library name is required.")
<<<<<<< HEAD
        if not latitude or not longitude:
            raise ValidationError("Latitude and longitude are required.")
=======
>>>>>>> fe008d114886a306d62feb191f3a0f6d32a4e575

        #sprawdzamy czy biblioteka już istnieje przy tworzeniu
        if Library.objects.filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city = request.data.get('city', instance.city).title()
        library_name = request.data.get('library_name', instance.library_name)
<<<<<<< HEAD
        lalitude = request.data.get('latitude', instance.latitude)
        longitude = request.data.get('longitude', instance.longitude)
=======
>>>>>>> fe008d114886a306d62feb191f3a0f6d32a4e575

        if not library_name:
            raise ValidationError("Library name is required.")

        if not city:
            raise ValidationError("City is required.")

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
        first_name = request.data.get('first_name', '').strip()
        second_name = request.data.get('second_name', '').strip()

        if not first_name:
            raise ValidationError("First name is required.")
        if not second_name:
            raise ValidationError("Second name is required.")

        existing_author = AuthorsDb.objects.filter(
            first_name__iexact=first_name,
            second_name__iexact=second_name
        ).first()

        if existing_author:
            return Response({
                'message': f'Autor {existing_author.first_name} {existing_author.second_name} już istnieje.',
                'id': existing_author.id,
            }, status=200)

        author_data = {
            'first_name': first_name.title(),
            'second_name': second_name.title(),
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

        # Sprawdzenie, czy tytuł jest pusty
        title = data.get('title', '').strip()
        if not title:
            return Response({"error": "Title cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)


        # Sprawdzanie, czy przynajmniej jedno z pól ISBN jest wypełnione
        isbn = data.get('isbn', '').strip()
        isbn13 = data.get('isbn13', '').strip()
        if not isbn and not isbn13:
            return Response({"error": "Either ISBN or ISBN-13 is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzenie, czy data publikacji jest pusta
        publication_date = data.get('publication_date', '').strip()
        if not publication_date:
            return Response({"error": "Publication date cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)


        # Automatyczne przekształcanie ISBN-10 do ISBN-13 i odwrotnie
        isbn = data.get('isbn', '').strip()
        isbn13 = data.get('isbn13', '').strip()

        if isbn and len(isbn) == 10:
            # Przekształcenie ISBN-10 do ISBN-13
            data['isbn13'] = '978' + isbn[:-1]  # Dodaj '978' i usuń ostatnią cyfrę ISBN-10
        elif isbn13 and len(isbn13) == 13:
            # Przekształcenie ISBN-13 do ISBN-10
            if isbn13.startswith('978'):
                data['isbn'] = isbn13[3:]  # Usuń '978' z ISBN-13
            else:
                return Response({"error": "Invalid ISBN-13 format. It should start with '978'."}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid ISBN format."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzenie, czy książka o tym samym tytule, ISBN i autorze już istnieje
        existing_book = BooksDb.objects.filter(title__iexact=data.get('title'),isbn=data.get('isbn'),author=author).first()
        if existing_book:
            return Response({
                "message": "Książka już istnieje.",
                "id": existing_book.id,
                "title": existing_book.title,
                "isbn": existing_book.isbn
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        book = self.get_object()  # Pobierz obiekt książki
        data = request.data.copy()  # Skopiuj dane żądania

        # Sprawdzenie, czy tytuł jest pusty
        title = data.get('title', '').strip()
        if title:
            book.title = title  # Ustaw nowy tytuł

        # Sprawdzenie, czy autor jest w danych żądania
        author_id = data.get('author')
        if author_id:
            try:
                author = AuthorsDb.objects.get(id=author_id)
                book.author = author  # Ustaw nowego autora
            except AuthorsDb.DoesNotExist:
                return Response({"error": "Author does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Sprawdzanie i aktualizacja ISBN oraz ISBN-13
        isbn = data.get('isbn', '').strip()
        isbn13 = data.get('isbn13', '').strip()

        # Walidacja i automatyczne ustawianie ISBN i ISBN-13
        if isbn:
            if len(isbn) != 10:
                return Response({"error": "ISBN must be 10 characters."}, status=status.HTTP_400_BAD_REQUEST)
            book.isbn = isbn  # Ustaw ISBN

        if isbn13:
            if not isbn13.startswith('978') or len(isbn13) != 13:
                return Response({"error": "ISBN-13 must start with '978' and be 13 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            book.isbn13 = isbn13  # Ustaw ISBN-13
            if not isbn:  # Automatycznie uzupełnij ISBN, jeśli nie jest podany
                book.isbn = isbn13[3:]  # Usuń '978' z ISBN-13

        # Sprawdzenie daty publikacji
        publication_date = data.get('publication_date', '').strip()
        if publication_date:
            book.publication_date = publication_date  # Ustaw datę publikacji

        # Sprawdzenie, czy ocena jest w danych żądania
        rating = data.get('rating')
        if rating is not None:
            try:
                rating = float(rating)
                if 1.0 <= rating <= 5.0:
                    book.rating = rating  # Ustaw nową ocenę
                else:
                    return Response({"error": "Rating must be between 1.0 and 5.0."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Invalid rating format."}, status=status.HTTP_400_BAD_REQUEST)

        # Zapisz zmiany w obiekcie książki
        book.save()  # Zapisz wszystkie zmiany

        return Response({"message": "Book updated successfully.", "book": book.title}, status=status.HTTP_200_OK)

    # def update(self, request, *args, **kwargs):
    #     book = self.get_object()  # Pobierz obiekt książki
    #     rating = request.data.get('rating')  # Pobierz ocenę z danych żądania

    #     if rating is None:
    #         return Response({"error": "Rating is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         rating = float(rating)
    #         if 1.0 <= rating <= 5.0:
    #             book.rating = rating  # Ustaw nową ocenę
    #             book.save()  # Zapisz zmiany
    #             return Response({"message": "Rating updated successfully.", "new_rating": book.rating}, status=status.HTTP_200_OK)
    #         else:
    #             return Response({"error": "Rating must be between 1.0 and 5.0."}, status=status.HTTP_400_BAD_REQUEST)
    #     except ValueError:
    #         return Response({"error": "Invalid rating format."}, status=status.HTTP_400_BAD_REQUEST)



    # @action(detail=True, methods=['patch'])
    # def update_rating(self, request, pk=None):
    #     book = self.get_object()
    #     rating = request.data.get('rating')

    #     if rating is not None:
    #         try:
    #             # Zakładam, że rating to float
    #             book.rating = rating
    #             book.save()
    #             return Response({"message": "Rating updated successfully."}, status=status.HTTP_200_OK)
    #         except Exception as e:
    #             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({"error": "Rating is required."}, status=status.HTTP_400_BAD_REQUEST)


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
