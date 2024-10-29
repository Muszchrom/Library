from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.decorators import api_view
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
    RentalsDb,
)

from .serializers import (
    LibrarySerializer, 
    AuthorsDbSerializer, 
    BooksDbSerializer,
    GenresDbSerializer,
    BookGenresDbSerializer,
    LibraryBooksDbSerializer,
    RentalsDbSerializer,
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


'''             TWORZENIE AUTORÓW           '''
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

    # def delete(self, request):
    #     AuthorsDb.objects.all().delete()
    #     return Response({"message": "All authors deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


'''             TWORZENIE GATUNKÓW           '''
class CreateGenres(APIView):
    genres_data = [
        {"genre": "Fantastyka"},
        {"genre": "Powieść psychologiczna"},
        {"genre": "Kryminał"},
        {"genre": "Romans"},
        {"genre": "Powieść historyczna"},
        {"genre": "Powieść "},
        {"genre": "Literatura współczesna"},
        {"genre": "Reportaż"},
        {"genre": "Psychologia"},
        {"genre": "Literatura piękna"},
        {"genre": "Literatura młodzieżowa"},
        {"genre": "Science fiction"},
        {"genre": "Horror"},
    ]

    def get(self, request):
        created, skipped = self.create_genres()
        return Response(
            {
                "message": "Genres processed successfully!",
                "created": created,
                "skipped": skipped,
            },
            status=status.HTTP_200_OK  # Użyj HTTP_200_OK dla poprawnych zapytań GET
        )

    def create_genres(self):

        created_genres = []
        skipped_genres = []

        for genre in self.genres_data:
            if GenresDb.objects.filter(genre__iexact=genre['genre']).exists():  # Użyj 'genre' zamiast 'name'
                skipped_genres.append(genre['genre'])
            else:
                serializer = GenresDbSerializer(data=genre)
                if serializer.is_valid():
                    serializer.save()
                    created_genres.append(genre['genre'])
                else:
                    print(serializer.errors)  # Log błędów

        return created_genres, skipped_genres


'''             TWORZENIE KSIĄŻEK           '''
class CreateBooks(APIView):
    books_data = [
{
        "id": 1,
        "author": 1,
        "isbn": "8377995817",
        "isbn13": "9788377995817",
        "title": "Czarny Pająk",
        "description": "Opowieść o zmaganiach z mrocznymi siłami.",
        "publication_date": "2015-03-30",
        "rating": "4.0"
    },
    {
        "id": 2,
        "author": 2,
        "isbn": "8324028620",
        "isbn13": "9788324028620",
        "title": "Zbrodnia I Kara",
        "description": "Klasyczna powieść o moralnych dylematach.",
        "publication_date": "1886-01-01",
        "rating": "4.5"
    },
    {
        "id": 3,
        "author": 3,
        "isbn": "8324028873",
        "isbn13": "9788324028873",
        "title": "Cicha Noc",
        "description": "Kryminał osadzony w przedwojennym Krakowie.",
        "publication_date": "2015-11-25",
        "rating": "4.0"
    },
    {
        "id": 4,
        "author": 3,
        "isbn": "8366089258",
        "isbn13": "9788366089258",
        "title": "Wielka Samotność",
        "description": "Historia miłości i przetrwania w trudnych czasach.",
        "publication_date": "2018-04-01",
        "rating": "4.5"
    },
    {
        "id": 5,
        "author": 48,
        "isbn": "8381981077",
        "isbn13": "9788381981077",
        "title": "Księgi Jakubowe",
        "description": "Epicka powieść o Jakubie Franku.",
        "publication_date": "2014-04-15",
        "rating": "5.0"
    },
    {
        "id": 6,
        "author": 5,
        "isbn": "8365999915",
        "isbn13": "9788365999915",
        "title": "Małe Życie",
        "description": "Opowieść o przyjaźni i traumach.",
        "publication_date": "2015-03-04",
        "rating": "4.0"
    },
    {
        "id": 7,
        "author": 6,
        "isbn": "8376270063",
        "isbn13": "9788376270063",
        "title": "Przeminęło Z Wiatrem",
        "description": "Powieść o miłości i wojnie secesyjnej.",
        "publication_date": "1936-01-01",
        "rating": "3.0"
    },
    {
        "id": 8,
        "author": 48,
        "isbn": "8377540366",
        "isbn13": "9788377540366",
        "title": "Bieguni",
        "description": "Książka o podróżnikach i ich losach.",
        "publication_date": "2007-03-01",
        "rating": "5.0"
    },
    {
        "id": 9,
        "author": 8,
        "isbn": "8380493674",
        "isbn13": "9788380493674",
        "title": "Wojna Nie Ma W Sobie Nic Z Kobiety",
        "description": "Reportaż o kobietach w czasie II wojny światowej.",
        "publication_date": "1985-01-01",
        "rating": "5.0"
    },
    {
        "id": 10,
        "author": 7,
        "isbn": "8375032518",
        "isbn13": "9788375032518",
        "title": "Człowiek W Poszukiwaniu Sensu",
        "description": "Książka o sensie życia w obliczu cierpienia.",
        "publication_date": "1946-01-01",
        "rating": "3.5"
    },
    {
        "id": 11,
        "author": 9,
        "isbn": "8388581686",
        "isbn13": "9788388581686",
        "title": "Sztuka Kochania",
        "description": "Książka o miłości i relacjach międzyludzkich.",
        "publication_date": "1975-01-01",
        "rating": "4.5"
    },
    {
        "id": 12,
        "author": 10,
        "isbn": "8381981718",
        "isbn13": "9788381981718",
        "title": "Córka",
        "description": "Opowieść o relacjach rodzinnych.",
        "publication_date": "2003-01-01",
        "rating": "4.0"
    },
    {
        "id": 13,
        "author": 11,
        "isbn": "8375082376",
        "isbn13": "9788375082376",
        "title": "Duma I Uprzedzenie",
        "description": "Klasyczna powieść o miłości i klasach społecznych.",
        "publication_date": "1813-01-28",
        "rating": "3.5"
    },
    {
        "id": 14,
        "author": 12,
        "isbn": "8371415177",
        "isbn13": "9788371415177",
        "title": "Na Wschód Od Edenu",
        "description": "Powieść o konflikcie dobra i zła w Kalifornii.",
        "publication_date": "1952-01-01",
        "rating": "4.0"
    },
    {
        "id": 15,
        "author": 13,
        "isbn": "8375103421",
        "isbn13": "9788375103421",
        "title": "Rok 1984",
        "description": "Dystopijna wizja totalitarnego państwa.",
        "publication_date": "1949-01-01",
        "rating": "3.0"
    },
    {
        "id": 16,
        "author": 14,
        "isbn": "8380017937",
        "isbn13": "9788380017937",
        "title": "Lalka",
        "description": "Powieść o życiu polskiego chłopstwa.",
        "publication_date": "1890-01-01",
        "rating": "5.0"
    },
    {
        "id": 17,
        "author": 15,
        "isbn": "8377651831",
        "isbn13": "9788377651831",
        "title": "Lśnienie",
        "description": "Powieść grozy o zjawiskach paranormalnych.",
        "publication_date": "1977-01-01",
        "rating": "3.5"
    }
    ]
    def get(self, request):
        created, skipped = self.create_books()
        return Response(
            {
                "message": "Books processed successfully!",
                "created": created,
                "skipped": skipped,
            },
            status=status.HTTP_200_OK  
        )

    def create_books(self):
        created_books = []
        skipped_books = []

        for book in self.books_data:
            if BooksDb.objects.filter(isbn=book['isbn']).exists():
                skipped_books.append(book['title'])
            else:
                serializer = BooksDbSerializer(data=book)
                if serializer.is_valid():
                    serializer.save()
                    created_books.append(book['title'])
                else:
                    print(serializer.errors)  

        return created_books, skipped_books


'''             TWORZENIE KSIĄŻEK           '''
class CreateBookGenres(APIView):
    # Example data structure for book-genre relationships
    books_genres_data = [
    {
        "book": 1,
        "genre": 1
    },
    {
        "book": 2,
        "genre": 2
    },
    {
        "book": 3,
        "genre": 3
    },
    {
        "book": 4,
        "genre": 4
    },
    {
        "book": 5,
        "genre": 5
    },
    {
        "book": 6,
        "genre": 6
    },
    {
        "book": 7,
        "genre": 5
    },
    {
        "book": 8,
        "genre": 6
    },
    {
        "book": 9,
        "genre": 7
    },
    {
        "book": 10,
        "genre": 8
    },
    {
        "book": 11,
        "genre": 9
    },
    {
        "book": 12,
        "genre": 10
    },
    {
        "book": 13,
        "genre": 9
    },
    {
        "book": 15,
        "genre": 11
    },
    {
        "book": 16,
        "genre": 13
    },
    {
        "book": 17,
        "genre": 12
    }
    ]

    def get(self, request):
        created, skipped = self.create_book_genres()
        return Response(
            {
                "message": "Book-Genre relationships processed successfully!",
                "created": created,
                "skipped": skipped,
            },
            status=status.HTTP_200_OK
        )

    def create_book_genres(self):
        created_entries = []
        skipped_entries = []

        for entry in self.books_genres_data:
            book_id = entry["book"]
            genre_id = entry["genre"]

            if BookGenresDb.objects.filter(book_id=book_id, genre_id=genre_id).exists():
                skipped_entries.append(entry)
            else:

                serializer = BookGenresDbSerializer(data=entry)
                if serializer.is_valid():
                    serializer.save()
                    created_entries.append(entry)
                else:
                    print(serializer.errors)  

        return created_entries, skipped_entries