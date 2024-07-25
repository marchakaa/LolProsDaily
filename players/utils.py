import random
from .models import Player

def get_random_player():
    players = Player.objects.filter(is_active=True)
    if players.exists():
        return random.choice(players)
    return None
