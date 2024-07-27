from django.shortcuts import render
from django.http import JsonResponse
from .models import Player

from django.core.cache import cache
from datetime import datetime
from .utils import get_random_player

from random import choice

from .country import get_country_code

def home(request):
    # Clear guessed players for home mode on each load
    request.session['guessed_players_home'] = []

    daily_player = get_daily_player()
    context = {
        'daily_player': daily_player,
    }
    return render(request, 'home.html', context)


def practice(request):
    # Clear guessed players for practice mode on each load
    request.session['guessed_players_practice'] = []

    # Optionally, get a new random player for practice mode
    get_random_player_each_refresh()
    return render(request, 'practice.html')
def all_pros(request):
    players = Player.objects.all()
    for player in players:
        player.country_code = get_country_code(player.nationality)
    
    context = {
        'players': players,
    }
    return render(request, 'all_pros.html', context)

def guess_player(request):
    if request.method == 'GET':
        player_name = request.GET.get('name', '').strip()
        page_type = request.GET.get('page_type', 'home')

        if page_type == 'home':
            daily_player = get_daily_player()
            session_key = 'daily_guessed_players'
        else:
            daily_player = get_random_player_each_refresh()
            session_key = 'practice_guessed_players'

        if session_key not in request.session:
            request.session[session_key] = []

        response_data = {
            'correct': False,
            'attributes': {}
        }

        if player_name in request.session[session_key]:
            response_data['message'] = 'You have already guessed this player.'
        else:
            try:
                guessed_player = Player.objects.get(name__iexact=player_name)

                request.session[session_key].append(player_name)
                request.session.modified = True

                response_data['attributes'] = {
                    'name': guessed_player.name,
                    'nationality': guessed_player.nationality,
                    'current_team': guessed_player.current_team,
                    'league': guessed_player.league,
                    'is_active': guessed_player.is_active,
                    'role': guessed_player.role
                }

                response_data['comparisons'] = {
                    'nationality': guessed_player.nationality == daily_player.nationality,
                    'current_team': guessed_player.current_team == daily_player.current_team,
                    'league': guessed_player.league == daily_player.league,
                    'is_active': guessed_player.is_active == daily_player.is_active,
                    'role': guessed_player.role == daily_player.role
                }

                if player_name.lower() == daily_player.name.lower():
                    response_data['message'] = 'Player found!'
                    response_data['correct'] = True
                else:
                    response_data['message'] = 'Incorrect guess! Try again.'
            except Player.DoesNotExist:
                response_data['message'] = 'Player not found in the database.'

        return JsonResponse(response_data)
    
def get_daily_player():
    today = datetime.now().date()
    cache_key = f"daily_player_{today}"
    player = cache.get(cache_key)

    if player is None:
        player = get_random_player()
        if player:
            cache.set(cache_key, player, 86400)  # Съхранява се за 24 часа
    return player

def get_random_player_each_refresh():
    players = Player.objects.all()
    if players:
        return choice(players)
    return None