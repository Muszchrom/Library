from rest_framework import serializers
from .models import Library, AuthorsDb, BooksDb

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','library_name','city']

class AuthorsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorsDb
        fields = ['id', 'first_name', 'second_name']

class BooksDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksDb
        fields = ['id', 'author_id', 'isbn', 'isbn13', 'title', 'description', 'publication_date']