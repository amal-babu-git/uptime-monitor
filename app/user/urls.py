from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Cutomized jwt auth with simple jwt TODO: Experimental
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import MyTokenObtainPairView, UserViewSet

rounter = DefaultRouter()
rounter.register('', UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(rounter.urls)),
]
