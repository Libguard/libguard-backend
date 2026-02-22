from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)


    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


    def __str__(self) -> str:
        return f"Name: {self.name}"
    



"""
class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Vulnerabilidades
    name = models.TextField() # Titulo da vulnerabilidade
    vulnerability_id = models.CharField(max_length=100)
    severity = models.CharField(max_length=50)
    vulnerability_description = models.TextField() # O campo 'Description' do JSON do Trivy
    primary_url = models.URLField()
    # FALTA A VERSÃO #

    # Pacote afetado
    package_name = models.CharField(max_length=200)
    package_id = models.CharField(max_length=100)
    fixed_version = models.CharField(max_length=200)

    # Dados usados para a análise
    target = models.CharField(max_length=60) # Lockfile usado no projeto
    package_manager = models.CharField(max_length=20) # Package manager utilizado no projeto

    # Metadados
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField()
"""