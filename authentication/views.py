from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer


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


class LogoutView(APIView):
    """View für den Logout. Blacklistet den Refresh-Token und löscht Cookies."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Macht den Refresh-Token ungültig und entfernt die Auth-Cookies."""
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. "
                       "Refresh token is now invalid."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CookieTokenRefreshView(APIView):
    """View für den Token-Refresh. Liest den Refresh-Token aus dem Cookie."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Erzeugt einen neuen Access-Token aus dem Refresh-Cookie."""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            access_token = token.access_token
        except TokenError:
            return Response(
                {"detail": "Refresh token invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"detail": "Token refreshed"},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=settings.COOKIE_HTTPONLY,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
        )
        return response
