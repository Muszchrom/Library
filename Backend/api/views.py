from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Library, AuthorsDb, BooksDb
from .serializers import LibrarySerializer, AuthorsDbSerializer, BooksDbSerializer


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()  # Zachowaj oryginalne queryset
        city = self.request.query_params.get('city', None)  # Pobierz parametr city z zapytania
        if city is not None:
            queryset = queryset.filter(city__iexact=city)  # Filtrowanie bibliotek po mieście
            if not queryset.exists():  # Sprawdź, czy nie znaleziono żadnych bibliotek
                return Response({"detail": "No libraries found in this city."}, status=status.HTTP_404_NOT_FOUND)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        identifier = kwargs.get('pk')                                                 # nazwa lub di
        try:
            if identifier.isdigit():                                                  #jako id
                instance = Library.objects.get(id=int(identifier))
            else:  
                instance = Library.objects.get(library_name__iexact=identifier)       #jako nazwa

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Library.DoesNotExist:
            raise NotFound(detail="Library NOT found.")


class AuthorsDbViewSet(viewsets.ModelViewSet):
    queryset = AuthorsDb.objects.all()
    serializer_class = AuthorsDbSerializer

class BooksDbViewSet(viewsets.ModelViewSet):
    queryset = BooksDb.objects.all()
    serializer_class = BooksDbSerializer