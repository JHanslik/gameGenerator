from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('my-games/', views.my_games, name='my_games'),
    path('create/', views.game_create, name='game_create'),
    path('create-random/', views.random_game_create, name='random_game_create'),
    path('favorites/', views.favorites, name='favorites'),
    path('<slug:slug>/', views.game_detail, name='game_detail'),
    path('<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/toggle-public/', views.toggle_public, name='toggle_public'),
]
