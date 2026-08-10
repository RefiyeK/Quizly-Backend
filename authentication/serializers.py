from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user.
    Validates the input data and creates a new user.
    """

    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Check whether both passwords match."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                "The passwords do not match."
            )
        return data

    def validate_email(self, value):
        """Check whether the email is already registered."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already in use."
            )
        return value

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop('confirmed_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class LoginSerializer(TokenObtainPairSerializer):
    """Serializer for login. Validates credentials and adds user data."""

    def validate(self, attrs):
        """Validate the credentials and add the user data."""
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data
