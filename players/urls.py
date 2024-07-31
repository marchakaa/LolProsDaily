from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('all_pros/', views.all_pros, name='all_pros'),
    path('guess_player/', views.guess_player, name='guess_player'),
    path('search_players/', views.search_players, name='search_players'),
]
