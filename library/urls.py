from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet,
    AuthorViewSet,
    CategoryViewSet,
    PublishingViewSet,
    LocationViewSet,
    ReviewViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'publishings', PublishingViewSet, basename='publishing')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
