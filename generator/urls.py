from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('game/<int:game_id>/generate/', views.generate_game_content, name='generate_game_content'),
    path('game/<int:game_id>/image/<str:type>/', views.generate_image, name='generate_image'),
    path('status/<int:request_id>/', views.generation_status, name='generation_status'),
]
