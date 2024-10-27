from rest_framework import serializers
from .models import Library, AuthorsDb, BooksDb, GenresDb, BookGenresDb, LibraryBooksDb, RentalsDb

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
        fields = ['id', 'author', 'isbn', 'isbn13', 'title', 'description', 'publication_date','rating']

    def validate(self, data):
        # Sprawdzanie, czy książka już istnieje
        if BooksDb.objects.filter(isbn=data['isbn'], author=data['author']).exists():
            raise serializers.ValidationError("This book with the same ISBN by this author already exists.")
        return data

    def validate_isbn(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("ISBN must be 10 characters long.")
        return value

    def validate_isbn13(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN13 must be 13 characters long.")
        return value

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value.title()  

    def validate_rating(self, value):                                                                   #sprawdzenie poprawności opinii
        if value is not None and (value < 1 or value > 5 or (value * 2) % 1 != 0):
            raise serializers.ValidationError("Ocena musi być liczbą od 1 do 5, z krokiem 0.5")
        return value

class GenresDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenresDb  
        fields = ['id', 'genre']
    
    def validate_genre(self, value):    
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")
        
        formatted_value = value.title()
        if GenresDb.objects.filter(genre__iexact=formatted_value).exists():
            raise serializers.ValidationError("This genre already exists.")
        return formatted_value

class BookGenresDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenresDb
        fields = '__all__'
        #fields = ['book', 'genre']
        #fields = ['book_id', 'genre_id']

    def create(self, validated_data):
        book = validated_data.get('book')
        genre = validated_data.get('genre')

        # Sprawdź, czy relacja już istnieje
        if BookGenresDb.objects.filter(book=book, genre=genre).exists():
            raise serializers.ValidationError("Ta relacja już istnieje.")

        return super().create(validated_data)

class LibraryBooksDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBooksDb
        fields = '__all__'
        # fields = ['book_id', 'library_id', 'book_count']
        
    def validate_book_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Book count cannot be negative.")
        return value

class RentalsDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalsDb
        fields = '__all__'
        #fields = ['id', 'user_id', 'book_id', 'library_id', 'rental_status', 'rental_date', 'due_date', 'return_date']