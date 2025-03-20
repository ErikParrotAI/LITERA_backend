from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author, Category, Publishing, Location, Review
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublishingSerializer,
    LocationSerializer,
    ReviewSerializer
)
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('publishing', 'location').prefetch_related('authors', 'categories')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter
    ordering_fields = ['year_of_publication', 'name', 'number_of_pages']
    ordering = ['name']  # сортування за замовчуванням

    def get_queryset(self):
        # Використовуємо select_related для ForeignKey полів (publishing, location)
        # та prefetch_related для ManyToMany полів (authors, categories)
        return Book.objects.all().select_related('publishing', 'location').prefetch_related('authors', 'categories')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


@api_view(['GET'])
def autocomplete_suggestions(request):
    search_term = request.query_params.get('search', '').strip()
    if not search_term:
        return Response([])

    suggestions = set()

    # 1) Назви книжок
    book_names = Book.objects.filter(name__icontains=search_term).values_list('name', flat=True)
    suggestions.update(book_names)

    # 2) Імена авторів
    author_names = Author.objects.filter(full_name__icontains=search_term).values_list('full_name', flat=True)
    suggestions.update(author_names)

    # 3) Назви видавництв
    publishing_names = Publishing.objects.filter(name__icontains=search_term).values_list('name', flat=True)
    suggestions.update(publishing_names)

    # 4) Назви категорій
    category_names = Category.objects.filter(name__icontains=search_term).values_list('name', flat=True)
    suggestions.update(category_names)

    # 5) Назви локацій
    location_names = Location.objects.filter(name__icontains=search_term).values_list('name', flat=True)
    suggestions.update(location_names)

    # Формуємо відсортований список, обрізаємо до 10 результатів
    suggestions_list = sorted(suggestions)[:10]

    return Response(suggestions_list)


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
