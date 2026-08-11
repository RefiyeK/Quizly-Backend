from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def set_token_cookie(response, key, value):
    """Write a single JWT token as an HttpOnly cookie on the response."""
    response.set_cookie(
        key=key,
        value=str(value),
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )


def blacklist_token(refresh_token):
    """Blacklist a refresh token, ignoring missing or invalid tokens."""
    if not refresh_token:
        return
    try:
        RefreshToken(refresh_token).blacklist()
    except TokenError:
        pass
