from django.urls import path, include
from .views import TokenObtainPairView


urlpatterns = [
    path('jwt/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]