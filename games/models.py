from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Game(models.Model):
    """Modèle principal pour les jeux générés"""
    GENRE_CHOICES = [
        ('rpg', 'RPG'),
        ('fps', 'FPS'),
        ('strategy', 'Stratégie'),
        ('platformer', 'Plateformes'),
        ('adventure', 'Aventure'),
        ('simulation', 'Simulation'),
        ('puzzle', 'Puzzle'),
        ('metroidvania', 'Metroidvania'),
        ('visual_novel', 'Visual Novel'),
        ('other', 'Autre'),
    ]
    
    AMBIANCE_CHOICES = [
        ('post_apo', 'Post-apocalyptique'),
        ('cyberpunk', 'Cyberpunk'),
        ('fantasy', 'Fantasy'),
        ('medieval', 'Médiéval'),
        ('sci_fi', 'Science-Fiction'),
        ('horror', 'Horreur'),
        ('steampunk', 'Steampunk'),
        ('noir', 'Noir/Detective'),
        ('western', 'Western'),
        ('dreamlike', 'Onirique'),
        ('other', 'Autre'),
    ]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    ambiance = models.CharField(max_length=20, choices=AMBIANCE_CHOICES)
    keywords = models.CharField(max_length=200)
    cultural_references = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le slug si non défini"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Assure l'unicité du slug
            while Game.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            self.slug = slug
        
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']

class GameDetail(models.Model):
    """Détails complets du jeu généré"""
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='detail')
    universe_description = models.TextField(blank=True)
    plot = models.TextField(blank=True)
    act1 = models.TextField(blank=True)
    act2 = models.TextField(blank=True)
    act3 = models.TextField(blank=True)
    
    def __str__(self):
        return f"Détails de {self.game.title}"

class Character(models.Model):
    """Personnages du jeu"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    background = models.TextField()
    abilities = models.TextField()
    image = models.ImageField(upload_to='characters/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.game.title})"

class Location(models.Model):
    """Lieux du jeu"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='locations/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.game.title})"

class GameImage(models.Model):
    """Images associées au jeu"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='games/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image de {self.game.title}"

class Favorite(models.Model):
    """Système de favoris"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'game')
    
    def __str__(self):
        return f"{self.user.username} ♥ {self.game.title}"
