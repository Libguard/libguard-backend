from apps.accounts.models import User, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from apps.authentication.models import RefreshToken as RefreshModel
from django.db import transaction
from django.core.exceptions import ValidationError
import hashlib

def _gen_tokens(user:  User, ip):
    refresh = RefreshToken.for_user(user=user)
    access = refresh.access_token

    hash_token = hashlib.sha256(str(refresh).encode()).hexdigest()
    # esse de cima salva o token do usuario no banco de dados
    print(user)
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
