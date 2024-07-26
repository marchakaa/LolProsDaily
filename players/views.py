from django.shortcuts import render
from django.http import JsonResponse
from .models import Player

from django.core.cache import cache
from datetime import datetime
from .utils import get_random_player

from random import choice

from .country import get_country_code

def home(request):
    if 'guessed_players' in request.session:
        del request.session['guessed_players']
    return render(request, 'home.html')

def practice(request):
    # Logic for practice mode
    if 'guessed_players' in request.session:
        del request.session['guessed_players']
    get_random_player_each_refresh();
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
        daily_player = get_daily_player()

        if 'guessed_players' not in request.session:
            request.session['guessed_players'] = []

        response_data = {
            'correct': False,
            'attributes': {}
        }

        if player_name in request.session['guessed_players']:
            response_data['message'] = 'You have already guessed this player.'
        else:
            if daily_player:
                try:
                    guessed_player = Player.objects.get(name__iexact=player_name)

                    # Добавяне на играча в сесията
                    request.session['guessed_players'].append(player_name)
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
            else:
                response_data['message'] = 'No player found for today.'

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