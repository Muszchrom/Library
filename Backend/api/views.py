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

        #sprawdzanie pustych pól
        if not city:
            raise ValidationError("City is required.")
        if not library_name:
            raise ValidationError("Library name is required.")

        #sprawdzamy czy biblioteka już istnieje przy tworzeniu
        if Library.objects.filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city = request.data.get('city', instance.city).title()
        library_name = request.data.get('library_name', instance.library_name)

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

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_rating(self, request, pk=None):
        book = self.get_object()
        rating = request.data.get('rating')

        if rating is not None:
            try:
                # Zakładam, że rating to float
                book.rating = rating
                book.save()
                return Response({"message": "Rating updated successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Rating is required."}, status=status.HTTP_400_BAD_REQUEST)


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
