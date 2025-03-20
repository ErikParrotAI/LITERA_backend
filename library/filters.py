import django_filters
from django.db.models import Q
from .models import Book


class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_all', label='Пошук')
    min_year = django_filters.NumberFilter(field_name='year_of_publication', lookup_expr='gte', label='Рік від')
    max_year = django_filters.NumberFilter(field_name='year_of_publication', lookup_expr='lte', label='Рік до')
    min_pages = django_filters.NumberFilter(field_name='number_of_pages', lookup_expr='gte', label='Сторінок від')
    max_pages = django_filters.NumberFilter(field_name='number_of_pages', lookup_expr='lte', label='Сторінок до')

    class Meta:
        model = Book
        fields = []  # ми явно визначаємо необхідні фільтри

    def filter_all(self, queryset, name, value):
        """
        Шукаємо за усіма полями (OR): назва, автор, країна автора, видавництво, країна видавництва,
        категорії, мова, локація.
        """
        return queryset.filter(
            Q(name__icontains=value) |
            Q(authors__full_name__icontains=value) |
            Q(authors__country__name__icontains=value) |
            Q(publishing__name__icontains=value) |
            Q(publishing__country__name__icontains=value) |
            Q(categories__name__icontains=value) |
            Q(language__icontains=value) |
            Q(location__name__icontains=value)
        ).distinct()