from rest_framework import viewsets
from rest_framework import status

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
        queryset = super().get_queryset()                                       # oryginalny queryset
        city = self.request.query_params.get('city', None)                      # Pobierz parametr city z zapytania
        if city is not None:
            city = city.title()
            queryset = queryset.filter(city__iexact=city)                       # Filtrowanie bibliotek po mieście
            if not queryset.exists():  
                raise NotFound(detail=f"No libraries found in {city}.")      # 
        return queryset

    def create(self, request, *args, **kwargs):
        city = request.data.get('city', '').title()
        library_name = request.data.get('library_name')
        if Library.objects.filter(library_name__iexact=library_name, city__iexact=city).exists():
            raise ValidationError(f"Library '{library_name}' already exists in {city}.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        city = request.data.get('city', instance.city).title()
        library_name = request.data.get('library_name', instance.library_name)
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


'''             OBSŁUGA WYPOŻYCZEŃ            '''
class RentalsDbViewSet(viewsets.ModelViewSet):
    queryset = RentalsDb.objects.all()
    serializer_class = RentalsDbSerializer



class CreateAuthors(APIView):
    authors_data = [
        {"first_name": "Jacek", "second_name": "Dukaj"},
        {"first_name": "Fiodor", "second_name": "Dostojewski"},
        {"first_name": "Krzysztof", "second_name": "Beśka"},
        {"first_name": "Kristin", "second_name": "Hannah"},
        {"first_name": "Hanya", "second_name": "Yanagihara"},
        {"first_name": "Margaret", "second_name": "Mitchell"},
        {"first_name": "Viktor", "second_name": "Frankl"},
        {"first_name": "Svetlana", "second_name": "Aleksievich"},
        {"first_name": "Wisława", "second_name": "Szymborska"},
        {"first_name": "Dorota", "second_name": "Terakowska"},
        {"first_name": "Jane", "second_name": "Austen"},
        {"first_name": "John", "second_name": "Steinbeck"},
        {"first_name": "George", "second_name": "Orwell"},
        {"first_name": "Bolesław", "second_name": "Prus"},
        {"first_name": "Stephen", "second_name": "King"},

        ##fantastyka
        {"first_name": "J.R.R.", "second_name": "Tolkien"},
        {"first_name": "George R.R.", "second_name": "Martin"},
        {"first_name": "J.K.", "second_name": "Rowling"},
        {"first_name": "Patrick", "second_name": "Rothfuss"},
        {"first_name": "Leigh", "second_name": "Bardugo"},
        {"first_name": "Brandon", "second_name": "Sanderson"},

        ###powieść psychologiczna
        {"first_name": "Fyodor", "second_name": "Dostoevsky"},
        {"first_name": "Virginia", "second_name": "Woolf"},
        {"first_name": "Franz", "second_name": "Kafka"},
        {"first_name": "Sylvia", "second_name": "Plath"},
        {"first_name": "Kazuo", "second_name": "Ishiguro"},
        {"first_name": "Haruki", "second_name": "Murakami"},
        
        ## kryminał
        {"first_name": "Agatha", "second_name": "Christie"},
        {"first_name": "Arthur", "second_name": "Conan Doyle"},
        {"first_name": "Gillian", "second_name": "Flynn"},
        {"first_name": "Raymond", "second_name": "Chandler"},
        {"first_name": "James", "second_name": "Ellroy"},
        {"first_name": "Tess", "second_name": "Gerritsen"},
        {"first_name": "Patricia", "second_name": "Highsmith"},
        {"first_name": "Henning", "second_name": "Mankell"},
        {"first_name": "Harlan", "second_name": "Coben"},
        {"first_name": "Donna", "second_name": "Tartt"},

        ## romans
        {"first_name": "Jane", "second_name": "Austen"},
        {"first_name": "Nicholas", "second_name": "Sparks"},
        {"first_name": "E.L.", "second_name": "James"},
        {"first_name": "Diana", "second_name": "Gabaldon"},
        {"first_name": "Colleen", "second_name": "Hoover"},
        {"first_name": "Kristin", "second_name": "Hannah"},
        {"first_name": "Agnieszka", "second_name": "Krawczyk"},
        {"first_name": "Natasza", "second_name": "Socha"},
        {"first_name": "Katarzyna", "second_name": "Bonda"},
        {"first_name": "Dorota", "second_name": "Terakowska"},

        ## poweieść historyczna
        {"first_name": "Henryk", "second_name": "Sienkiewicz"},
        {"first_name": "Ken", "second_name": "Follett"},
        {"first_name": "Umberto", "second_name": "Eco"},
        {"first_name": "Olga", "second_name": "Tokarczuk"},
        {"first_name": "Bernard", "second_name": "Cornwell"},

        ## reportaż
        {"first_name": "Olga", "second_name": "Tokarczuk"},
        {"first_name": "Hanya", "second_name": "Yanagihara"},
        {"first_name": "David", "second_name": "Foster Wallace"},
        {"first_name": "Svetlana", "second_name": "Aleksievich"},
        {"first_name": "Haruki", "second_name": "Murakami"},

        ## Reportaż
        {"first_name": "Svetlana", "second_name": "Aleksievich"},
        {"first_name": "Ryszard", "second_name": "Kapuściński"},
        {"first_name": "Mariusz", "second_name": "Szczygieł"},
        {"first_name": "Hannah", "second_name": "Arendt"},
        {"first_name": "Truman", "second_name": "Capote"},
        {"first_name": "John", "second_name": "Hersey"},
        {"first_name": "Lynn", "second_name": "Perry"},
        {"first_name": "Barbara", "second_name": "Włodarczyk"},


        ## Psychologia
        {"first_name": "Sigmund", "second_name": "Freud"},
        {"first_name": "Carl", "second_name": "Jung"},
        {"first_name": "Albert", "second_name": "Ellis"},
        {"first_name": "Brené", "second_name": "Brown"},
        {"first_name": "Irvin", "second_name": "D. Yalom"},
        {"first_name": "Maria", "second_name": "Zsuzsanna"},
        {"first_name": "Wojciech", "second_name": "Eichelberger"},
        {"first_name": "Anna", "second_name": "Szmigiel"},


        ##Literatura piękna
        {"first_name": "Wisława", "second_name": "Szymborska"},
        {"first_name": "Olga", "second_name": "Tokarczuk"},
        {"first_name": "Bolesław", "second_name": "Prus"},
        {"first_name": "Jacek", "second_name": "Dukaj"},
        {"first_name": "Marcel", "second_name": "Proust"},
        {"first_name": "Gabriel", "second_name": "García Márquez"},
        {"first_name": "Virginia", "second_name": "Woolf"},
        {"first_name": "James", "second_name": "Joyce"},


        ## literatura młodzieżowa
        {"first_name": "Michał", "second_name": "Cholewa"},
        {"first_name": "Joanne", "second_name": "Rowling"},
        {"first_name": "John", "second_name": "Green"},
        {"first_name": "Katherine", "second_name": "Applegate"},
        {"first_name": "Tadeusz", "second_name": "Różewicz"},
        {"first_name": "Maggie", "second_name": "Stiefvater"},
        {"first_name": "Cassandra", "second_name": "Clare"},
        {"first_name": "Harlan", "second_name": "Coben"},

        ## science fiction
        {"first_name": "Stanislaw", "second_name": "Lem"},
        {"first_name": "Isaac", "second_name": "Asimov"},
        {"first_name": "Philip", "second_name": "K. Dick"},
        {"first_name": "Arthur", "second_name": "C. Clarke"},
        {"first_name": "Ursula", "second_name": "K. Le Guin"},
        {"first_name": "H.G.", "second_name": "Wells"},
        {"first_name": "Andrzej", "second_name": "Sapkowski"},
        {"first_name": "Margaret", "second_name": "Atwood"},

        ## horror
        {"first_name": "Stephen", "second_name": "King"},
        {"first_name": "H.P.", "second_name": "Lovecraft"},
        {"first_name": "Clive", "second_name": "Barker"},
        {"first_name": "Shirley", "second_name": "Jackson"},
        {"first_name": "Bram", "second_name": "Stoker"},
        {"first_name": "Anne", "second_name": "Rice"},
        {"first_name": "Jakub", "second_name": "Ćwiek"},
        {"first_name": "Maja", "second_name": "Lidia Kossakowska"},
    ]

    def get(self, request):
        created, skipped = self.create_authors()
        return Response(
            {"message": "Authors processed successfully!", "created": created, "skipped": skipped},
            status=status.HTTP_201_CREATED
        )

    def create_authors(self):
        created_authors = []
        skipped_authors = []
        
        for author in self.authors_data:
            if AuthorsDb.objects.filter(first_name=author['first_name'], second_name=author['second_name']).exists():

                skipped_authors.append(author)
            else:

                serializer = AuthorsDbSerializer(data=author)
                if serializer.is_valid():
                    serializer.save()
                    created_authors.append(author)
                else:
                    print(serializer.errors)  # Można także dodać logowanie błędów

        return created_authors, skipped_authors

    def delete(self, request):
        AuthorsDb.objects.all().delete()
        return Response({"message": "All authors deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

