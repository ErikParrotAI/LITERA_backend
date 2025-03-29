import django_filters
from .models import Book
from rapidfuzz import fuzz


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
        default_threshold = 80  # первинний поріг схожості
        books = list(queryset)
        scores_list = []

        for book in books:
            scores = []

            # Порівнюємо назву книги використовуючи partial_ratio
            if book.name:
                scores.append(fuzz.partial_ratio(book.name.lower(), value.lower()))

            # Порівнюємо імена авторів та країни авторів
            for author in book.authors.all():
                if author.full_name:
                    scores.append(fuzz.partial_ratio(author.full_name.lower(), value.lower()))
                if hasattr(author, 'country') and author.country and getattr(author.country, 'name', None):
                    scores.append(fuzz.partial_ratio(author.country.name.lower(), value.lower()))

            # Порівнюємо назву видавництва та країну видавництва
            if book.publishing and book.publishing.name:
                scores.append(fuzz.partial_ratio(book.publishing.name.lower(), value.lower()))
                if hasattr(book.publishing, 'country') and book.publishing.country and getattr(book.publishing.country, 'name', None):
                    scores.append(fuzz.partial_ratio(book.publishing.country.name.lower(), value.lower()))

            # Порівнюємо категорії
            for category in book.categories.all():
                if category.name:
                    scores.append(fuzz.partial_ratio(category.name.lower(), value.lower()))

            # Порівнюємо мову
            if book.language:
                scores.append(fuzz.partial_ratio(book.language.lower(), value.lower()))

            # Порівнюємо локацію
            if book.location and book.location.name:
                scores.append(fuzz.partial_ratio(book.location.name.lower(), value.lower()))

            max_score = max(scores) if scores else 0
            scores_list.append((book.pk, max_score))

        filtered_ids = [book_pk for book_pk, score in scores_list if score >= default_threshold]
        return queryset.filter(pk__in=filtered_ids)