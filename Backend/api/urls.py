from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import LibraryViewSet,AuthorsDbViewSet, BooksDbViewSet, BestSellerBooksViewSet, GenreDbViewSet, BookGenresDbViewSet, LibraryBooksDbViewSet, BestNearestView, RentalsDbViewSet, TestHeaderView

from .dev_views import generateTemplateData



router = DefaultRouter()
router.register(r'libraries', views.LibraryViewSet)
router.register(r'authors', views.AuthorsDbViewSet)
router.register(r'books', views.BooksDbViewSet)
#router.register(r'books/genres', views.GenreDbViewSet) =====> JESZCZE NIE DZIAŁA
router.register(r'genres', views.GenreDbViewSet, basename='genres')
router.register(r'book-genres', views.BookGenresDbViewSet)  
router.register(r'library-books', views.LibraryBooksDbViewSet)
router.register(r'rentals', views.RentalsDbViewSet)  
router.register(r'rentals', RentalsDbViewSet, basename='rentals')

router.register(r'bestseller', BestSellerBooksViewSet, basename='bestseller-books')
  


urlpatterns = [
    path('', include(router.urls)),
    
    path('libraries/<str:pk>/', LibraryViewSet.as_view({'get': 'retrieve'}), name='library-by-identifier'), 
    path('libraries/<int:library_id>/books/', views.BooksDbViewSet.as_view({'get': 'list'}), name='library-books'),   # Lista książek w bibliotece
    path('books/<int:pk>/update-rating/', BooksDbViewSet.as_view({'patch': 'update_rating'}), name='update-rating'),    #update rating
    path('libraries/<int:library_id>/books/', views.BooksDbViewSet.as_view({'get': 'list'}), name='library-books'),
    #generowanie danych
    path('generate', generateTemplateData),
    path('best-nearest/', BestNearestView.as_view(), name='best-nearest'),
    path('test-header/', TestHeaderView.as_view(), name='test-header'),

    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

