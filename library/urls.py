from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    LocationViewSet,
    ReviewViewSet,
    autocomplete_suggestions
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('autocomplete/', autocomplete_suggestions, name='autocomplete'),
]
