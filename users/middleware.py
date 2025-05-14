from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class RequireLoginMiddleware:
    """
    Middleware qui exige que l'utilisateur soit connecté pour accéder à toutes les pages
    sauf celles explicitement autorisées dans PUBLIC_PATHS.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Chemins qui sont accessibles sans connexion
        self.public_paths = [
            '/users/login/',
            '/users/register/',
            '/admin/',  # Admin Django
            '/admin/login/',
            '/static/',  # Fichiers statiques
            '/media/',  # Fichiers média
        ]
    
    def __call__(self, request):
        # Si l'utilisateur n'est pas connecté et n'accède pas à un chemin public
        if not request.user.is_authenticated:
            # Vérifier si le chemin actuel est public
            is_public = False
            path = request.path_info
            
            for public_path in self.public_paths:
                if path.startswith(public_path):
                    is_public = True
                    break
            
            # Si ce n'est pas un chemin public, rediriger vers la page de connexion
            if not is_public:
                return redirect(settings.LOGIN_URL + '?next=' + path)
        
        response = self.get_response(request)
        return response
