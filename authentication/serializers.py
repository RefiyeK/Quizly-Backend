from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer für die Registrierung eines neuen Benutzers.
    Validiert die Eingabedaten und erstellt einen neuen Benutzer.
    """

    confirmed_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validiert die Eingabedaten."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                "Die Passwörter stimmen nicht überein.")
        return data

    def validate_email(self, value):
        """ Validiert die E-Mail-Adresse des Benutzers.
        Überprüft, ob die E-Mail-Adresse bereits in der Datenbank vorhanden ist."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Diese E-Mail-Adresse ist bereits registriert.")
        return value

    def create(self, validated_data):
        """Erstellt einen neuen Benutzer mit den validierten Daten."""
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

        extra_kwargs = {
            'password': {'write_only': True}
        }
