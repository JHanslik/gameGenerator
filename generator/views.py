from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.files.base import ContentFile
from games.models import Game, GameDetail, Character, Location, GameImage
from .models import GenerationRequest, AIModel
from .services import HuggingFaceService

# Create your views here.

@login_required
def generate_game_content(request, game_id):
    """Vue pour générer du contenu pour un jeu existant"""
    game = get_object_or_404(Game, id=game_id)
    
    # Vérifier que l'utilisateur est le créateur du jeu
    if game.creator != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à générer du contenu pour ce jeu.")
        return redirect('games:game_list')
    
    # Créer une nouvelle requête de génération
    generation_request = GenerationRequest.objects.create(
        user=request.user,
        game=game,
        prompt=f"Générer du contenu pour {game.title}"
    )
    
    try:
        # Générer le contenu textuel
        HuggingFaceService.generate_game_content(generation_request)
        
        # Générer les images (en option, car cela peut prendre du temps)
        if request.GET.get('with_images', 'true') == 'true':
            HuggingFaceService.generate_game_images(game)
        
        messages.success(request, "Contenu généré avec succès !")
    except Exception as e:
        messages.error(request, f"Erreur lors de la génération : {str(e)}")
    
    return redirect('games:game_detail', slug=game.slug)

@login_required
def generate_image(request, game_id, type):
    """Vue pour générer une image (personnage ou lieu)"""
    game = get_object_or_404(Game, id=game_id, creator=request.user)
    
    # Vérifier si l'utilisateur peut faire des appels API
    if not request.user.profile.can_make_api_call():
        return JsonResponse({'error': 'Limite d\'API atteinte'}, status=403)
    
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if not prompt:
            return JsonResponse({'error': 'Prompt requis'}, status=400)
        
        try:
            # Générer l'image
            image_data = HuggingFaceService.generate_image(prompt)
            
            # Incrémenter le compteur d'appels API
            request.user.profile.increment_api_call()
            
            # Sauvegarder l'image selon le type
            if type == 'character':
                character_id = request.POST.get('character_id')
                character = get_object_or_404(Character, id=character_id, game=game)
                character.image.save(f"{character.name}.png", ContentFile(image_data), save=True)
                
            elif type == 'location':
                location_id = request.POST.get('location_id')
                location = get_object_or_404(Location, id=location_id, game=game)
                location.image.save(f"{location.name}.png", ContentFile(image_data), save=True)
                
            elif type == 'game':
                caption = request.POST.get('caption', '')
                game_image = GameImage(game=game, caption=caption)
                game_image.image.save(f"{game.title}_{timezone.now().timestamp()}.png", ContentFile(image_data), save=True)
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

@login_required
def generation_status(request, request_id):
    """Vue pour vérifier le statut d'une génération"""
    generation_request = get_object_or_404(GenerationRequest, id=request_id, user=request.user)
    
    return JsonResponse({
        'status': generation_request.status,
        'completed_at': generation_request.completed_at.isoformat() if generation_request.completed_at else None,
        'error_message': generation_request.error_message,
        'result': generation_request.result_json
    })
