from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    """Extension du modèle User pour stocker des informations supplémentaires"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    api_call_count = models.IntegerField(default=0)
    api_call_limit = models.IntegerField(default=50)  # Limite quotidienne
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def can_make_api_call(self):
        """Vérifie si l'utilisateur peut faire un appel à l'API"""
        return self.api_call_count < self.api_call_limit
    
    def increment_api_call(self):
        """Incrémente le compteur d'appels à l'API"""
        self.api_call_count += 1
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil quand un utilisateur est créé"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand l'utilisateur est sauvegardé"""
    instance.profile.save()
