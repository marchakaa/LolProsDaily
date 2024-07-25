from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guess_player/', views.guess_player, name='guess_player'),
]
