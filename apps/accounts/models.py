from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from rest_framework import serializers

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        return self.create_user(email, name, password, **extra_fields)

# Modelagem
class User(AbstractUser):
    # user é padrão do django-bomba, tirar ele
    username = None

    # atributos
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)

    # infos pro sistema
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email' # diz pro django q nao vai usar o username e sim o campo email
    REQUIRED_FIELDS = ['name'] # obrigatorio pedir o name

    class Meta:
        db_table = "users"
        verbose_name = 'User'        
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "name",
            "is_active",
            "created_at",
        ]