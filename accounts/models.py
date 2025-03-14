from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)

    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    x_link = models.URLField(unique=True, blank=True, null=True)
    instagram_link = models.URLField(unique=True, blank=True, null=True)
    telegram_link = models.URLField(unique=True, blank=True, null=True)
    facebook_link = models.URLField(unique=True, blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_private = models.BooleanField(default=False, help_text="Встановіть, якщо профіль має бути приватним")

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username


class Friendship(models.Model):
    class FriendshipStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        ACCEPTED = 'A', 'Accepted'
        DECLINED = 'D', 'Declined'
        BLOCKED = 'B', 'Blocked'

    user_from = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='friendships_sent'
    )
    user_to = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='friendships_received'
    )
    status = models.CharField(
        max_length=1,
        choices=FriendshipStatus.choices,
        default=FriendshipStatus.PENDING
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f"Friendship from {self.user_from} to {self.user_to} ({self.get_status_display()})"