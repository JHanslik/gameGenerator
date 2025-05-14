import os
import json
import time
import requests
from datetime import datetime
from django.conf import settings
from .models import GenerationRequest

class HuggingFaceService:
    """Service pour interagir avec les APIs de Hugging Face"""
    
    @staticmethod
    def generate_game_content(generation_request):
        """Génère du contenu pour un jeu via l'API Hugging Face"""
        try:
            # Marquer la requête comme en cours de traitement
            generation_request.status = 'processing'
            generation_request.save()
            
            # Préparer le prompt pour l'API
            game = generation_request.game
            prompt = f"""
            Génère un concept de jeu vidéo avec les caractéristiques suivantes:
            - Titre: {game.title}
            - Genre: {game.get_genre_display()}
            - Ambiance: {game.get_ambiance_display()}
            - Mots-clés: {game.keywords}
            - Références: {game.cultural_references}
            - Description de base: {game.description}
            
            Réponds uniquement au format JSON avec les champs suivants:
            - universe_description: description détaillée de l'univers du jeu (300-500 mots)
            - plot: intrigue principale du jeu (300-500 mots)
            - act1: description de l'acte 1 du jeu (200-300 mots)
            - act2: description de l'acte 2 du jeu (200-300 mots)
            - act3: description de l'acte 3 du jeu (200-300 mots)
            - characters: liste de 2-4 personnages, chacun avec nom, rôle, background et abilities
            - locations: liste de 2-3 lieux importants, chacun avec nom et description
            """
            
            # Appel à l'API de Hugging Face
            API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
            headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
            payload = {"inputs": prompt, "parameters": {"max_length": 4096, "return_full_text": False}}
            
            response = requests.post(API_URL, headers=headers, json=payload)
            response_json = response.json()
            
            # Extraction du texte de la réponse
            if isinstance(response_json, list) and len(response_json) > 0:
                generated_text = response_json[0].get("generated_text", "")
            else:
                generated_text = response_json.get("generated_text", "")
            
            # Extraction du JSON de la réponse texte
            import re
            json_match = re.search(r'{.*}', generated_text, re.DOTALL)
            if json_match:
                result_json = json.loads(json_match.group(0))
            else:
                # Si pas de JSON valide, créer une structure minimale
                result_json = {
                    "universe_description": "Impossible de générer une description.",
                    "plot": "Impossible de générer une intrigue.",
                    "act1": "", "act2": "", "act3": "",
                    "characters": [], "locations": []
                }
            
            # Mise à jour de la requête
            generation_request.status = 'completed'
            generation_request.completed_at = datetime.now()
            generation_request.result_json = result_json
            generation_request.save()
            
            return result_json
            
        except Exception as e:
            # En cas d'erreur
            generation_request.status = 'failed'
            generation_request.error_message = str(e)
            generation_request.save()
            raise e

    @staticmethod
    def generate_image(prompt, style="digital art", model="stabilityai/stable-diffusion-2-1"):
        """Génère une image via l'API Hugging Face"""
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
        
        # Amélioration du prompt pour de meilleurs résultats
        enhanced_prompt = f"{prompt}, {style}, high quality, detailed"
        
        # Appel à l'API
        response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
        
        # Vérification de la réponse
        if response.status_code != 200:
            error_msg = f"Erreur API: {response.status_code} - {response.text}"
            raise Exception(error_msg)
            
        return response.content  # Contenu binaire de l'image
