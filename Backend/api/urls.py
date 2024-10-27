from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import LibraryViewSet, BooksDbViewSet, GenreDbViewSet, BookGenresDbViewSet, LibraryBooksDbViewSet, CreateAuthors




router = DefaultRouter()
router.register(r'libraries', views.LibraryViewSet)
router.register(r'authors', views.AuthorsDbViewSet)
router.register(r'books', views.BooksDbViewSet)
#router.register(r'books/genres', views.GenreDbViewSet) =====> JESZCZE NIE DZIAŁA
router.register(r'genres', views.GenreDbViewSet, basename='genres')
router.register(r'book-genres', views.BookGenresDbViewSet)  
router.register(r'library-books', views.LibraryBooksDbViewSet)
router.register(r'rentals', views.RentalsDbViewSet)    


urlpatterns = [
    path('', include(router.urls)),
    path('libraries/<str:pk>/', LibraryViewSet.as_view({'get': 'retrieve'}), name='library-by-identifier'), 
    path('libraries/<int:library_id>/books/', views.BooksDbViewSet.as_view({'get': 'list'}), name='library-books'),   # Lista książek w bibliotece

    path('books/<int:pk>/update-rating/', BooksDbViewSet.as_view({'patch': 'update_rating'}), name='update-rating'),    #update rating

    path('create-authors/', CreateAuthors.as_view(), name='create-authors'),
 


    #path('books/genres/', views.GenreDbViewSet.as_view({'get': 'list'}), name='genre-list'),  t
    #path('books/genres/<str:pk>/', GenreDbViewSet.as_view({'get': 'retrieve'}), name='genre-detail'),


    #path('books/genres/<str:genre_name>/', GenreDbViewSet.as_view({'get': 'retrieve_by_genre_name'}), name='genre-by-name'),
    #path('books/<int:book_id>/rentals/', views.RentalsDbViewSet.as_view({'post': 'create'}), name='rent-book'),  # Wypożyczenie książki
    #path('rentals/<int:rental_id>/return/', views.RentalsDbViewSet.as_view({'post': 'return_book'}), name='return-book'),  # Zwrot książki
]

