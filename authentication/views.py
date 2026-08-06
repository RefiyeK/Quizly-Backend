from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .serializers import RegisterSerializer
from .serializers import LoginSerializer


class RegisterView(APIView):
    """View für die Registrierung eines neuen Benutzers."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validiert die Daten und erstellt einen neuen Benutzer."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "User created successfully!"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """View für den Login. Setzt Tokens als HttpOnly-Cookies."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validiert Zugangsdaten und setzt Auth-Cookies."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        response = Response(
            {"detail": "Login successfully!", "user": data['user']},
            status=status.HTTP_200_OK,
        )
        self._set_auth_cookies(response, data['access'], data['refresh'])
        return response

    def _set_auth_cookies(self, response, access, refresh):
        """Schreibt Access- und Refresh-Token als HttpOnly-Cookies."""
        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=settings.COOKIE_HTTPONLY,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=settings.COOKIE_HTTPONLY,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
        )
