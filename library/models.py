from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    work_schedule = models.CharField(max_length=100)
    longitude = models.DecimalField(
        max_digits=18,  # 3 знаки перед комою + 15 після коми
        decimal_places=15,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    latitude = models.DecimalField(
        max_digits=17,  # 2 знаки перед комою + 15 після коми
        decimal_places=15,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    instagram_link = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name


class Publishing(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    publishing = models.ForeignKey(Publishing, on_delete=models.SET_NULL, null=True)
    year_of_publication = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    number_of_pages = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='books')
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    locations = models.ManyToManyField('Location', related_name='books')

    def __str__(self):
        return self.name


class TradeLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    brought_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='brought_books')
    borrowed_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    trade_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Trade by {self.user} at {self.trade_time}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    response = models.TextField()
    writing_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.book}"
