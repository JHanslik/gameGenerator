from django.db import models
from django.contrib.auth.models import User
from games.models import Game

class GenerationRequest(models.Model):
    """Suivi des requêtes de génération"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generation_requests')
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, related_name='generation_requests')
    prompt = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    result_json = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"Génération {self.id} par {self.user.username} ({self.status})"
