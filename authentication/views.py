from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, LoginSerializer
from .utils import set_token_cookie, blacklist_token


class RegisterView(APIView):
    """View for registering a new user."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validate the data and create a new user."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "User created successfully!"},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """View for login. Sets tokens as HttpOnly cookies."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials and set auth cookies."""
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
        """Write the access and refresh tokens as HttpOnly cookies."""
        set_token_cookie(response, 'access_token', access)
        set_token_cookie(response, 'refresh_token', refresh)


class LogoutView(APIView):
    """View for logout. Blacklists the refresh token and deletes cookies."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Invalidate the refresh token and remove the auth cookies."""
        blacklist_token(request.COOKIES.get('refresh_token'))
        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. "
                       "Refresh token is now invalid."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CookieTokenRefreshView(APIView):
    """View for token refresh. Reads the refresh token from the cookie."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Create a new access token from the refresh cookie."""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            access_token = RefreshToken(refresh_token).access_token
        except TokenError:
            return Response(
                {"detail": "Refresh token invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        response = Response({"detail": "Token refreshed"},
                            status=status.HTTP_200_OK)
        set_token_cookie(response, 'access_token', access_token)
        return response
