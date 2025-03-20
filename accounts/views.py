from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, Friendship
from .serializers import CustomUserSerializer, FriendshipSerializer
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_info(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({"detail": "Старий пароль не вірний."}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password or len(new_password) < 8:
            return Response({"detail": "Новий пароль має бути не менше 8 символів."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Пароль успішно змінено."})


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user_from=user) | Friendship.objects.filter(user_to=user)

    def perform_create(self, serializer):
        serializer.save(user_from=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user_to != request.user:
            return Response({"detail": "Неможливо прийняти запит, який адресовано не вам."},
                            status=status.HTTP_403_FORBIDDEN)
        friendship.status = Friendship.FriendshipStatus.ACCEPTED
        friendship.save()
        return Response(self.get_serializer(friendship).data)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user_to != request.user:
            return Response({"detail": "Неможливо відхилити запит, який адресовано не вам."},
                            status=status.HTTP_403_FORBIDDEN)
        friendship.status = Friendship.FriendshipStatus.DECLINED
        friendship.save()
        return Response(self.get_serializer(friendship).data)

    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user_from != request.user:
            return Response({"detail": "Лише ініціатор запиту може заблокувати користувача."},
                            status=status.HTTP_403_FORBIDDEN)
        friendship.status = Friendship.FriendshipStatus.BLOCKED
        friendship.save()
        return Response(self.get_serializer(friendship).data)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refreshToken')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вихід успішний.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
