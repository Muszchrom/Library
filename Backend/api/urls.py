from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'libraries', views.LibraryViewSet)
router.register(r'authors', views.AuthorsDbViewSet)
router.register(r'books', views.BooksDbViewSet)

urlpatterns = [
    path('', include(router.urls)),
]