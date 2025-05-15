from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.files.base import ContentFile
from django.template.loader import get_template
from django.conf import settings
from django.contrib.staticfiles import finders
from games.models import Game, GameDetail, Character, Location, GameImage
from .models import GenerationRequest
from .services import HuggingFaceService
import os
import re
from io import BytesIO

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

def fetch_resources(uri, rel):
    """
    Récupère les ressources externes (images, CSS, etc.) pour xhtml2pdf
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ""))
    else:
        path = None
        
    if path:
        return path
    return uri

@login_required
def export_game_to_pdf(request, game_id):
    """Exporte un jeu au format PDF en utilisant xhtml2pdf"""
    game = get_object_or_404(Game, id=game_id)
    
    # Vérifier que l'utilisateur est le créateur du jeu ou que le jeu est public
    if game.creator != request.user and not game.is_public:
        messages.error(request, "Vous n'êtes pas autorisé à exporter ce jeu.")
        return redirect('games:game_list')
    
    try:
        # Importer la bibliothèque xhtml2pdf
        from xhtml2pdf import pisa
        
        # Préparer le contexte avec les URL absolues
        host = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'
        base_url = f"{protocol}://{host}"
        
        context = {
            'game': game,
            'request': request,
            'base_url': base_url,
            'MEDIA_URL': f"{base_url}{settings.MEDIA_URL}",
            'STATIC_URL': f"{base_url}{settings.STATIC_URL}",
        }
        
        # Rendre le template HTML avec le contexte
        template = get_template('games/export_pdf.html')
        html_string = template.render(context)
        
        # Remplacer les liens relatifs par des liens absolus pour les images
        html_string = re.sub(r'src="(/media/[^"]+)"', f'src="{base_url}\\1"', html_string)
        
        # Créer un buffer pour le PDF
        buffer = BytesIO()
        
        # Convertir le HTML en PDF avec gestion des ressources
        pisa_status = pisa.CreatePDF(
            html_string,
            dest=buffer,
            encoding='utf-8',
            link_callback=fetch_resources
        )
        
        # Vérifier si la conversion a réussi
        if pisa_status.err:
            messages.error(request, "Une erreur s'est produite lors de la génération du PDF.")
            return redirect('games:game_detail', slug=game.slug)
        
        # Réinitialiser le pointeur du buffer
        buffer.seek(0)
        
        # Traiter le nom du fichier pour éviter les caractères problématiques
        filename = re.sub(r'[^\w\s-]', '', game.title).replace(' ', '_')
        
        # Créer la réponse HTTP avec le contenu PDF
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}_GDD.pdf"'
        
        return response
        
    except ImportError:
        messages.error(request, "L'export PDF n'est pas disponible. Veuillez installer xhtml2pdf.")
        return redirect('games:game_detail', slug=game.slug)
    except Exception as e:
        messages.error(request, f"Une erreur s'est produite lors de l'export : {str(e)}")
        return redirect('games:game_detail', slug=game.slug)
