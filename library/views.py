from rest_framework import viewsets, permissions, filters
from .models import Book, Author, Category, Publishing, Location, Review
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublishingSerializer,
    LocationSerializer,
    ReviewSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'authors__full_name', 'publishing__name', 'categories__name', 'language']

    def get_queryset(self):
        # Використовуємо select_related для ForeignKey полів (publishing, location)
        # та prefetch_related для ManyToMany полів (authors, categories)
        return Book.objects.all().select_related('publishing', 'location').prefetch_related('authors', 'categories')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class PublishingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publishing.objects.all()
    serializer_class = PublishingSerializer
    permission_classes = [permissions.AllowAny]


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
