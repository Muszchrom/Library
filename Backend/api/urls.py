from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import LibraryViewSet, BooksDbViewSet


router = DefaultRouter()
router.register(r'libraries', views.LibraryViewSet)
router.register(r'authors', views.AuthorsDbViewSet)
router.register(r'books', views.BooksDbViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('libraries/<str:pk>/', LibraryViewSet.as_view({'get': 'retrieve'}), name='library-by-identifier'), 
]

