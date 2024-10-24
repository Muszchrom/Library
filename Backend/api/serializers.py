from rest_framework import serializers
from .models import Library, AuthorsDb, BooksDb
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id','library_name']
class AuthorsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorsDb
        fields = '__all__'
class BooksDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksDb
        fields = '__all__'