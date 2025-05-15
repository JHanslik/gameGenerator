from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from games.models import Favorite

# Create your views here.

def register_view(request):
    """Vue pour l'inscription des utilisateurs"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie ! Bienvenue sur GameForge.")
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """Vue pour la connexion des utilisateurs"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {username} !")
                # Redirection vers la page demandée ou la page d'accueil
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
        
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """Vue pour la déconnexion des utilisateurs"""
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

@login_required
def profile_view(request):
    """Vue pour afficher et modifier le profil utilisateur"""
    return render(request, 'users/profile.html')

@login_required
def dashboard_view(request):
    """Vue pour le tableau de bord utilisateur"""
    # Récupérer tous les jeux de l'utilisateur
    user_games = request.user.games.all()
    
    # Récupérer les favoris de l'utilisateur
    favorites = Favorite.objects.filter(user=request.user)
    
    # Compter les jeux publics de l'utilisateur
    public_games_count = user_games.filter(is_public=True).count()
    
    context = {
        'games': user_games,
        'favorites': favorites,
        'public_games_count': public_games_count
    }
    
    return render(request, 'users/dashboard.html', context)
