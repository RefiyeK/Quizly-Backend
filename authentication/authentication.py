from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """Liest den Access-Token aus dem HttpOnly-Cookie statt aus dem Header."""

    def authenticate(self, request):
        """Holt den Access-Token aus dem Cookie und validiert ihn."""
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)
        return (user, validated_token)