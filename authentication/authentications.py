from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            return f'Bearer {token}'.encode()
        return None