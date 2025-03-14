from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Friendship


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Перевірка облікових даних користувача за email та паролем.
        Оскільки за умовчанням Django використовує username для автентифікації,
        ми шукаємо користувача за email і перевіряємо пароль вручну.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Невірні облікові дані.")

        if not user.check_password(password):
            raise serializers.ValidationError("Невірні облікові дані.")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Після успішної автентифікації генеруємо JWT токени для користувача.
        """
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'accessToken': str(refresh.access_token),
            'refreshToken': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # За потребою можна додати інші поля користувача
            }
        }


class CustomUserSerializer(serializers.ModelSerializer):
    # Поле для аватара, якщо використовується MEDIA_URL для генерації URL
    avatar = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'x_link',
            'instagram_link',
            'telegram_link',
            'facebook_link',
            'avatar',
            'is_private',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        """
        Створення нового користувача.
        Пароль обробляється за допомогою set_password для безпечного хешування.
        """
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Оновлення даних користувача.
        Якщо передається новий пароль, він безпечно хешується.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class FriendshipSerializer(serializers.ModelSerializer):
    # Використовуємо CustomUserSerializer для відображення інформації про користувачів,
    # пов’язаних дружбою.
    user_from = CustomUserSerializer(read_only=True)
    user_to = CustomUserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'user_from', 'user_to', 'status', 'created', 'updated']
