from rest_framework import serializers
from .models import Country, Location, Author, Publishing, Category, Book, Review
from accounts.serializers import CustomUserSerializer  # для відображення автора відгуку


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'address', 'work_schedule']


class AuthorSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'full_name', 'date_of_birth', 'country']


class PublishingSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)

    class Meta:
        model = Publishing
        fields = ['id', 'name', 'country']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    # Використовуємо вкладені серіалізатори для відображення пов’язаних даних
    authors = AuthorSerializer(many=True, read_only=True)
    publishing = PublishingSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'name',
            'location',
            'authors',
            'publishing',
            'year_of_publication',
            'language',
            'number_of_pages',
            'categories'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    # Для відображення даних про користувача використовується CustomUserSerializer
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'book',
            'rating',
            'response',
            'writing_time'
        ]
