from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, FriendshipViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'friendships', FriendshipViewSet, basename='friendship')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
]
