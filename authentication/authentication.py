from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CookieJWTAuthentication(JWTAuthentication):
    """Reads the access token from the HttpOnly cookie instead of the header."""

    def authenticate(self, request):
        """Retrieve the access token from the cookie and validate it.

        Returns None if the token is missing or invalid, so that
        AllowAny endpoints (login, refresh) remain reachable.
        """
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
        except (InvalidToken, TokenError):
            return None

        return (user, validated_token)
