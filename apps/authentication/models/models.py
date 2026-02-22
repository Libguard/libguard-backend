from django.db import models
from apps.accounts.models import User

class RefreshToken (models.Model):
    id_token = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="refresh_tokens")

    hash_token = models.CharField(unique=True, max_length=255)
    ip = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "refresh_tokens"
        verbose_name = 'Refresh Token'        
        verbose_name_plural = 'Refresh Tokens'
    
    def __str__(self):
        return self.hash_token