import re
from rest_framework import serializers
from apps.accounts.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(required=True, min_length=8, max_length=16)

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    name = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, min_length=8, max_length=16)
    password_confirm = serializers.CharField(required=True, min_length=8, max_length=16)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este e-mail já está em uso')
        return value

    def validate(self, data):
        password = data['password']
        password_confirm = data['password_confirm']

        if password != password_confirm:
            raise serializers.ValidationError('As senhas não coincidem')
        if not re.search(r'[A-Z]', password):
            raise serializers.ValidationError('A senha precisa ter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', password):
            raise serializers.ValidationError('A senha precisa ter pelo menos uma letra minúscula')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise serializers.ValidationError('A senha precisa ter pelo menos um caractere especial (!@#$...)')
        return data