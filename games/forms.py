from django import forms
from .models import Game

class GameCreationForm(forms.ModelForm):
    """Formulaire pour créer un nouveau concept de jeu"""
    
    class Meta:
        model = Game
        fields = ['title', 'genre', 'ambiance', 'keywords', 'cultural_references', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Titre de votre jeu'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: boucle temporelle, vengeance, IA rebelle (séparés par des virgules)'
            }),
            'cultural_references': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Ex: Zelda, Hollow Knight, Disco Elysium (facultatif)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 4,
                'placeholder': 'Brève description de votre concept de jeu'
            }),
            'genre': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'ambiance': forms.Select(attrs={
                'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 rounded focus:ring-blue-500'
            })
        }
        labels = {
            'title': 'Titre',
            'genre': 'Genre',
            'ambiance': 'Ambiance',
            'keywords': 'Mots-clés thématiques',
            'cultural_references': 'Références culturelles',
            'description': 'Description',
            'is_public': 'Rendre public'
        }
        help_texts = {
            'keywords': 'Séparez les mots-clés par des virgules',
            'is_public': 'Si coché, votre jeu sera visible par tous les utilisateurs'
        }
