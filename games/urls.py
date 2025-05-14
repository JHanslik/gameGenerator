from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('my-games/', views.my_games, name='my_games'),
    path('create/', views.game_create, name='game_create'),
    path('<slug:slug>/', views.game_detail, name='game_detail'),
    path('<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
]
