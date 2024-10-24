from rest_framework import viewsets
from .models import Library, AuthorsDb, BooksDb
from .serializers import LibrarySerializer, AuthorsDbSerializer, BooksDbSerializer

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

class AuthorsDbViewSet(viewsets.ModelViewSet):
    queryset = AuthorsDb.objects.all()
    serializer_class = AuthorsDbSerializer
    
class BooksDbViewSet(viewsets.ModelViewSet):
    queryset = BooksDb.objects.all()
    serializer_class = BooksDbSerializer