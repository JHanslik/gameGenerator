from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game, GameDetail, Favorite
from .forms import GameCreationForm
from django.http import JsonResponse
import random

# Create your views here.

@login_required
def game_list(request):
    """Vue pour afficher la liste des jeux publics"""
    games = Game.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'games/game_list.html', {'games': games})

@login_required
def my_games(request):
    """Vue pour afficher les jeux créés par l'utilisateur"""
    games = Game.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'games/my_games.html', {'games': games})

@login_required
def game_create(request):
    """Vue pour créer un nouveau jeu"""
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            # Créer un objet Game mais ne pas le sauvegarder immédiatement
            game = form.save(commit=False)
            # Définir le créateur comme l'utilisateur actuel
            game.creator = request.user
            # Sauvegarder l'objet Game
            game.save()
            
            # Créer un GameDetail vide associé au jeu
            GameDetail.objects.create(game=game)
            
            messages.success(request, f"Votre jeu '{game.title}' a été créé avec succès!")
            
            # Rediriger vers la page de génération de contenu
            return redirect('games:game_detail', slug=game.slug)
    else:
        form = GameCreationForm()
    
    return render(request, 'games/game_create.html', {'form': form})

@login_required
def game_detail(request, slug):
    """Vue pour afficher les détails d'un jeu"""
    game = get_object_or_404(Game, slug=slug)
    
    # Vérifier si l'utilisateur a le droit de voir ce jeu
    if not game.is_public and game.creator != request.user:
        messages.error(request, "Vous n'avez pas l'autorisation de voir ce jeu.")
        return redirect('games:game_list')
    
    return render(request, 'games/game_detail.html', {'game': game})

@login_required
def toggle_favorite(request, slug):
    """Vue pour ajouter ou retirer un jeu des favoris"""
    game = get_object_or_404(Game, slug=slug)
    
    # Vérifier si ce jeu est déjà un favori pour cet utilisateur
    favorite, created = Favorite.objects.get_or_create(user=request.user, game=game)
    
    if not created:
        # Si le favori existait déjà, le supprimer
        favorite.delete()
        is_favorite = False
        messages.success(request, f"{game.title} a été retiré de vos favoris.")
    else:
        is_favorite = True
        messages.success(request, f"{game.title} a été ajouté à vos favoris.")
    
    # Si c'est une requête AJAX, renvoyer une réponse JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'is_favorite': is_favorite})
    
    # Sinon, rediriger vers la page précédente
    return redirect(request.META.get('HTTP_REFERER', 'games:game_detail'))

@login_required
def favorites(request):
    """Vue pour afficher les jeux favoris de l'utilisateur"""
    favorite_games = Game.objects.filter(favorited_by__user=request.user)
    return render(request, 'games/favorites.html', {'games': favorite_games})

@login_required
def random_game_create(request):
    """Vue pour créer un jeu aléatoire"""
    # Choisir un genre aléatoire
    genres = [choice[0] for choice in Game.GENRE_CHOICES]
    random_genre = random.choice(genres)
    
    # Choisir une ambiance aléatoire
    ambiances = [choice[0] for choice in Game.AMBIANCE_CHOICES]
    random_ambiance = random.choice(ambiances)
    
    # Liste de mots-clés potentiels
    keywords_options = [
        "exploration", "magie", "survie", "combat", "puzzle", "crafting", 
        "open-world", "narration", "multijoueur", "roguelike", "temps réel", 
        "tour par tour", "économie", "stratégie", "gestion", "compétition",
        "collaboration", "voyage", "mystère", "quête", "développement", "construction",
        "diplomatie", "infiltration", "course", "simulation", "action"
    ]
    
    # Sélectionner 2 à 4 mots-clés aléatoires
    num_keywords = random.randint(2, 4)
    random_keywords = ", ".join(random.sample(keywords_options, num_keywords))
    
    # Liste de références culturelles potentielles
    references_options = [
        "Star Wars", "Le Seigneur des Anneaux", "Harry Potter", "Marvel", 
        "Game of Thrones", "Cyberpunk", "Blade Runner", "Matrix", "Dune", 
        "Star Trek", "Lovecraft", "Mythologie nordique", "Mythologie grecque", 
        "Mythologie égyptienne", "Indiana Jones", "Zelda", "Final Fantasy",
        "Naruto", "One Piece", "Dragon Ball", "Dark Souls", "Mass Effect", 
        "Fallout", "The Witcher", "Skyrim", "Minecraft", "Mad Max", "Alien"
    ]
    
    # Sélectionner 1 à 2 références culturelles aléatoires
    num_references = random.randint(1, 2)
    random_references = ", ".join(random.sample(references_options, num_references))
    
    # Générer un titre aléatoire
    prefixes = ["Chroniques de", "Le Mystère de", "Aventures en", "L'Écho de", "La Quête de", "Les Légendes de", 
               "L'Épée de", "Royaume de", "Empire de", "Odyssée", "Guerriers de", "Éveil de", "Cité de"]
    suffixes = ["Destin", "Légende", "Monde", "Royaume", "Étoiles", "Âme", "Destinée", "Cristal", "Vengeance", 
               "Renaissance", "Prophétie", "Chaos", "Ombre", "Lumière", "Horizon", "Création", "Frontière"]
    
    random_title = f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    # Description de base aléatoire
    descriptions = [
        f"Un jeu {Game.GENRE_CHOICES[genres.index(random_genre)][1]} se déroulant dans un univers {Game.AMBIANCE_CHOICES[ambiances.index(random_ambiance)][1]}.",
        f"Plongez dans un monde {Game.AMBIANCE_CHOICES[ambiances.index(random_ambiance)][1]} avec ce jeu {Game.GENRE_CHOICES[genres.index(random_genre)][1]}.",
        f"Une aventure {Game.GENRE_CHOICES[genres.index(random_genre)][1]} épique dans un univers {Game.AMBIANCE_CHOICES[ambiances.index(random_ambiance)][1]}.",
        f"Découvrez un univers {Game.AMBIANCE_CHOICES[ambiances.index(random_ambiance)][1]} à travers cette expérience {Game.GENRE_CHOICES[genres.index(random_genre)][1]}."
    ]
    random_description = random.choice(descriptions)
    
    # Créer le jeu avec les attributs aléatoires
    game = Game(
        creator=request.user,
        title=random_title,
        genre=random_genre,
        ambiance=random_ambiance,
        keywords=random_keywords,
        cultural_references=random_references,
        description=random_description
    )
    game.save()
    
    # Créer un GameDetail vide associé au jeu
    GameDetail.objects.create(game=game)
    
    messages.success(request, f"Votre jeu aléatoire '{game.title}' a été créé avec succès! Générez maintenant du contenu pour lui donner vie.")
    
    # Rediriger vers la génération de contenu
    return redirect('generator:generate_game_content', game_id=game.id)
