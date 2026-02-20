from apps.accounts.models import User, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from datetime import timedelta
from apps.authentication.models import RefreshToken as RefreshModel
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from decouple import config
import hashlib

def _gen_tokens(user:  User, ip):
    refresh = RefreshToken.for_user(user=user)
    access = refresh.access_token

    hash_token = hashlib.sha256(str(refresh).encode()).hexdigest()
    # esse de cima salva o token do usuario no banco de dados
    RefreshModel.objects.create(
        user_id=user,
        hash_token=hash_token,
        ip=ip,
        expires_at=timezone.now() + timedelta(days=30)
    )

    return str(refresh), str(access)

@transaction.atomic # caso alguma das tentivas de criar um objeto der errado ele da um rollback
def create_user_service(email, name, password, ip): # vai chamar esse metodo, q vai chamar esse de cima 
    try:
        user = User.objects.create_user(
            email=email,
            name=name,
            password=password
        )

        refresh, access = _gen_tokens(user, ip)

        return {
            "refresh": refresh,
            "access": access,
            "user": UserSerializer(user).data
        }
    except Exception as e:
        raise ValidationError(f"Falha na criação do usuário: {str(e)}")

@transaction.atomic
def login_user_service(email, password, ip):
    try:
        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed("E-mail ou senha inválidos") 
        
        refresh, access = _gen_tokens(user= user, ip= ip)

        return {
            "refresh": refresh,
            "access": access,
            "user": UserSerializer(user).data
        }
    except AuthenticationFailed as e:
        raise e
    except Exception as e:
        raise ValidationError(f"Falha ao validar o usuário: {str(e)}")
    
@transaction.atomic
def refresh_token_service(refresh, ip):
    try:
        token = RefreshToken(refresh)

        hash_token = hashlib.sha256(refresh.encode()).hexdigest()

        stored_token = RefreshModel.objects.filter(
            hash_token= hash_token
        ).first()

        if not stored_token:
            raise AuthenticationFailed("Refresh token não reconhecido")
        
        if stored_token.expires_at < timezone.now():
            stored_token.delete()
            raise AuthenticationFailed("Refresh token expirado")
        
        if stored_token.ip != ip:
            stored_token.delete()
            raise AuthenticationFailed("Refresh token criado em outro IP.")
        
        user = stored_token.user_id
        stored_token.delete()

        refresh, access = _gen_tokens(user, ip)

        return {
            "refresh": refresh,
            "access": access
        }
    except Exception:
        raise AuthenticationFailed("Refresh token inválido")
    
@transaction.atomic
def google_login_service(code, ip):
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": config("GOOGLE_CLIENT_ID"),
        "client_secret": config("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": config("GOOGLE_REDIRECT_URI"),
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    if not response.ok:
        raise AuthenticationFailed(f"Erro na Google: {response.json().get('error_description')}")
    
    token_json = response.json()
    id_token_value = token_json.get("id_token")

    if not id_token_value:
        raise ValueError("id_token não recebido")
    
    try:
        id_info = id_token.verify_oauth2_token(
            id_token_value,
            google_requests.Request(),
            config("GOOGLE_CLIENT_ID"),
            clock_skew_in_seconds=10
        )
        
        user = User.objects.filter(email= id_info['email']).first()

        if not user:
            result = create_user_service(
                email=id_info['email'],
                name=id_info['name'],
                password=None,
                ip=ip
            )
            return result
        
        refresh, access = _gen_tokens(user=user, ip=ip)
        return {
            "refresh": refresh,
            "access": access,
            "user": user
        }
    except ValueError as e:
        raise AuthenticationFailed(f"Token inválido: {str(e)}")

    
    