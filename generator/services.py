import os
import json
import time
import requests
import logging
from datetime import datetime
from django.conf import settings
from .models import GenerationRequest
from games.models import GameDetail, Character, Location

# Configurez le logger
logger = logging.getLogger(__name__)

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
            
            logger.info(f"Prompt pour le jeu {game.title}: {prompt[:100]}...")
            
            # Vérifier la clé API
            api_key = settings.HUGGINGFACE_API_KEY
            if not api_key:
                logger.error("Clé API Hugging Face non configurée")
                raise ValueError("Clé API Hugging Face non configurée")
            
            logger.info(f"Utilisation de la clé API: {api_key[:5]}...")
            
            # Liste de modèles à essayer
            models_to_try = [
                "mistralai/Mistral-7B-v0.1",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "google/gemma-7b-it"
            ]
            
            response = None
            last_error = None
            
            # Essayer chaque modèle jusqu'à ce qu'un fonctionne
            for model in models_to_try:
                try:
                    API_URL = f"https://api-inference.huggingface.co/models/{model}"
                    headers = {"Authorization": f"Bearer {api_key}"}
                    payload = {"inputs": prompt, "parameters": {"max_length": 4096, "return_full_text": False}}
                    
                    logger.info(f"Tentative avec le modèle : {model}")
                    response = requests.post(API_URL, headers=headers, json=payload)
                    
                    if response.status_code == 200:
                        logger.info(f"Modèle {model} a répondu avec succès")
                        break
                    else:
                        last_error = f"Erreur API avec modèle {model}: {response.status_code} - {response.text}"
                        logger.warning(last_error)
                except Exception as e:
                    last_error = f"Exception avec modèle {model}: {str(e)}"
                    logger.exception(last_error)
            
            # Vérifier si on a obtenu une réponse valide
            if response is None or response.status_code != 200:
                error_msg = last_error or "Tous les modèles ont échoué"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            response_json = response.json()
            
            # Extraction du texte de la réponse
            if isinstance(response_json, list) and len(response_json) > 0:
                generated_text = response_json[0].get("generated_text", "")
            else:
                generated_text = response_json.get("generated_text", "")
            
            logger.info(f"Texte généré: {generated_text[:200]}...")
            
            # Extraction du JSON de la réponse texte
            import re
            json_match = re.search(r'{.*}', generated_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(0)
                logger.info(f"JSON extrait: {json_text[:200]}...")
                result_json = json.loads(json_text)
            else:
                logger.error("Pas de JSON valide trouvé dans la réponse")
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
            
            # Créer les détails du jeu
            game_detail, created = GameDetail.objects.get_or_create(game=game)
            game_detail.universe_description = result_json.get('universe_description', '')
            game_detail.plot = result_json.get('plot', '')
            game_detail.act1 = result_json.get('act1', '')
            game_detail.act2 = result_json.get('act2', '')
            game_detail.act3 = result_json.get('act3', '')
            game_detail.save()
            
            # Créer les personnages
            characters = result_json.get('characters', [])
            if isinstance(characters, list):
                # Supprimer les personnages existants pour éviter les doublons
                Character.objects.filter(game=game).delete()
                
                for character_data in characters:
                    if isinstance(character_data, dict):
                        Character.objects.create(
                            game=game,
                            name=character_data.get('name', 'Personnage sans nom'),
                            role=character_data.get('role', 'Rôle inconnu'),
                            background=character_data.get('background', ''),
                            abilities=character_data.get('abilities', '')
                        )
            
            # Créer les lieux
            locations = result_json.get('locations', [])
            if isinstance(locations, list):
                # Supprimer les lieux existants pour éviter les doublons
                Location.objects.filter(game=game).delete()
                
                for location_data in locations:
                    if isinstance(location_data, dict):
                        Location.objects.create(
                            game=game,
                            name=location_data.get('name', 'Lieu sans nom'),
                            description=location_data.get('description', '')
                        )
            
            return result_json
            
        except Exception as e:
            logger.exception(f"Erreur lors de la génération: {str(e)}")
            # En cas d'erreur
            generation_request.status = 'failed'
            generation_request.error_message = str(e)
            generation_request.save()
            raise e

    @staticmethod
    def generate_image(prompt, style="digital art", model="stabilityai/stable-diffusion-xl-base-1.0"):
        """Génère une image via l'API Hugging Face"""
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
            
            # Amélioration du prompt pour de meilleurs résultats
            enhanced_prompt = f"{prompt}, {style}, high quality, detailed"
            logger.info(f"Génération d'image avec prompt: {enhanced_prompt}")
            
            # Appel à l'API
            response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
            
            # Vérification de la réponse
            if response.status_code != 200:
                error_msg = f"Erreur API Image: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
            logger.info(f"Image générée avec succès, taille: {len(response.content)} bytes")
            return response.content  # Contenu binaire de l'image
            
        except Exception as e:
            logger.exception(f"Erreur lors de la génération d'image: {str(e)}")
            raise e

    @staticmethod
    def generate_game_images(game):
        """Génère des images pour un jeu (personnages et lieux)"""
        try:
            logger.info(f"Génération d'images pour le jeu: {game.title}")
            
            # Générer une image d'ambiance pour le jeu
            from django.core.files.base import ContentFile
            from games.models import GameImage
            
            # Image principale du jeu
            game_prompt = f"A {game.get_ambiance_display()} {game.get_genre_display()} video game concept art titled {game.title}"
            logger.info(f"Génération de l'image principale: {game_prompt}")
            
            try:
                game_image_content = HuggingFaceService.generate_image(game_prompt)
                game_image = GameImage(game=game, caption=f"Concept art principal de {game.title}")
                game_image.image.save(f"{game.slug}_main.png", ContentFile(game_image_content), save=True)
                logger.info(f"Image principale sauvegardée pour {game.title}")
            except Exception as e:
                logger.error(f"Échec de génération de l'image principale: {str(e)}")
            
            # Générer des images pour les personnages
            for character in game.characters.all():
                character_prompt = f"Character portrait of {character.name}, {character.role} in a {game.get_ambiance_display()} {game.get_genre_display()} game"
                logger.info(f"Génération d'image pour le personnage {character.name}: {character_prompt}")
                
                try:
                    character_image_content = HuggingFaceService.generate_image(character_prompt)
                    character.image.save(f"{game.slug}_{character.name.lower().replace(' ', '_')}.png", 
                                        ContentFile(character_image_content), save=True)
                    logger.info(f"Image sauvegardée pour le personnage {character.name}")
                except Exception as e:
                    logger.error(f"Échec de génération d'image pour {character.name}: {str(e)}")
            
            # Générer des images pour les lieux
            for location in game.locations.all():
                location_prompt = f"{location.name}, location in a {game.get_ambiance_display()} {game.get_genre_display()} game"
                logger.info(f"Génération d'image pour le lieu {location.name}: {location_prompt}")
                
                try:
                    location_image_content = HuggingFaceService.generate_image(location_prompt)
                    location.image.save(f"{game.slug}_{location.name.lower().replace(' ', '_')}.png", 
                                       ContentFile(location_image_content), save=True)
                    logger.info(f"Image sauvegardée pour le lieu {location.name}")
                except Exception as e:
                    logger.error(f"Échec de génération d'image pour {location.name}: {str(e)}")
            
            logger.info(f"Génération d'images terminée pour le jeu {game.title}")
            return True
            
        except Exception as e:
            logger.exception(f"Erreur lors de la génération des images du jeu: {str(e)}")
            return False
