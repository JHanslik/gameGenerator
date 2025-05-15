from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from games.models import Game, GameDetail

# Create your tests here.

class PDFExportTest(TestCase):
    def setUp(self):
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Créer un jeu de test
        self.game = Game.objects.create(
            title="Test Game",
            description="This is a test game",
            genre="FPS",
            ambiance="SCI_FI",
            keywords="test, example",
            creator=self.user,
            is_public=True
        )
        
        # Créer le détail du jeu
        GameDetail.objects.create(
            game=self.game,
            universe_description="Test universe description",
            plot="Test plot"
        )
        
        # Créer un client
        self.client = Client()
    
    def test_pdf_export_authenticated(self):
        """Tester que l'export PDF fonctionne pour un utilisateur authentifié"""
        # S'authentifier
        self.client.login(username='testuser', password='testpassword123')
        
        # Accéder à l'URL d'export PDF
        response = self.client.get(reverse('generator:export_pdf', kwargs={'game_id': self.game.id}))
        
        # Vérifier que la réponse est un PDF
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue('attachment; filename=' in response['Content-Disposition'])
    
    def test_pdf_export_unauthorized(self):
        """Tester que l'accès à l'export PDF est refusé pour un jeu privé"""
        # Rendre le jeu privé
        self.game.is_public = False
        self.game.save()
        
        # Créer un autre utilisateur
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        
        # S'authentifier avec l'autre utilisateur
        self.client.login(username='otheruser', password='otherpassword123')
        
        # Accéder à l'URL d'export PDF
        response = self.client.get(reverse('generator:export_pdf', kwargs={'game_id': self.game.id}))
        
        # Vérifier que l'accès est redirigé (car non autorisé)
        self.assertEqual(response.status_code, 302)
