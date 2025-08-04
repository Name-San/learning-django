from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView

class TokenObtainPairView(BaseTokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        response.set_cookie(
            key='access_token',
            value=access_token,
            max_age=24*60*60,
            secure=True,
            httponly=True,
            samesite='Strict'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            max_age=24*60*60,
            secure=True,
            httponly=True,
            samesite='Strict'
        )

        return response