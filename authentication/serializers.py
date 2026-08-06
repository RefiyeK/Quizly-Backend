from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer für die Registrierung eines neuen Benutzers.
    Validiert die Eingabedaten und erstellt einen neuen Benutzer.
    """

    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Prüft, ob beide Passwörter übereinstimmen."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                "Die Passwörter stimmen nicht überein."
            )
        return data

    def validate_email(self, value):
        """Prüft, ob die E-Mail bereits registriert ist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Diese E-Mail wird bereits verwendet."
            )
        return value

    def create(self, validated_data):
        """Erstellt einen neuen Benutzer mit gehashtem Passwort."""
        validated_data.pop('confirmed_password')
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
    """Serializer für den Login. Validiert Zugangsdaten und erzeugt Tokens."""

    def validate(self, attrs):
        """Prüft die Zugangsdaten und ergänzt die Nutzerdaten."""
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data