from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError

from .models import (
    Library, 
    AuthorsDb, 
    BooksDb
)

from .serializers import (
    LibrarySerializer, 
    AuthorsDbSerializer, 
    BooksDbSerializer
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
        # Tworzenie kopii request.data jako słownik
        data = request.data.copy()
        author_id = data.get('author')  # Oczekujemy ID autora jako string

        if author_id:
            try:
                author = AuthorsDb.objects.get(id=author_id)
                data['author'] = author.id  # Przypisz ID autora do skopiowanych danych
            except AuthorsDb.DoesNotExist:
                return Response({"error": "Author does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Author is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)  # Użyj skopiowanych danych
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)