import sys
import os
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist

# Get the current file's directory and set up Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lolprosdaily.settings")

import django
django.setup()

from players.models import Player
# Define the path for the players file
PLAYERS_FILE = os.path.join(project_root, "players.txt")

def read_players_from_file():
    """Reads the players from the players.txt file and returns a set of player names."""
    if not os.path.exists(PLAYERS_FILE):
        return set()
    with open(PLAYERS_FILE, 'r', encoding='utf-8') as file:
        return set(line.split(';')[0] for line in file)
    
def read_players_info_from_file():
    """Reads the players from the players.txt file and returns a list of player information."""
    if not os.path.exists(PLAYERS_FILE):
        return []
    
    with open(PLAYERS_FILE, 'r', encoding='utf-8') as file:
        players_info = [tuple(line.strip().split(';')) for line in file]
    
    return players_info
    
def write_player_to_file(player_name, nationality, current_team, role, image_url, is_active):
    """Writes a player's details to the players.txt file."""
    with open(PLAYERS_FILE, 'a', encoding='utf-8') as file:
        file.write(f"{player_name};{nationality};{current_team};{role};{image_url};{is_active}\n")

def get_player_info(player_name):
    # Format the URL
    url = f"https://lol.fandom.com/wiki/{player_name}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        return f"Failed to retrieve data for {player_name}. Status code: {response.status_code}"
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the infobox table
    infobox = soup.find('table', class_='infobox-player-narrow')
    
    if not infobox:
        return f"Could not find player information for {player_name}"
    
    # Initialize variables
    country_of_birth = "Not found"
    role = "Not found"
    team = "Not found"
    image_url = "Not found"
    
    # Extract the image URL
    image_element = infobox.find('img')
    if image_element and 'src' in image_element.attrs:
        image_url = image_element['src']
    
    # Extract the other information
    rows = infobox.find_all('tr')
    for row in rows:
        label = row.find('td', class_='infobox-label')
        if label:
            if label.text.strip() == "Country of Birth":
                country_of_birth = row.find('td', class_='infobox-label').find_next_sibling('td').text.strip()
            elif label.text.strip() == "Role":
                role = row.find('td', class_='infobox-label').find_next_sibling('td').text.strip()
            elif label.text.strip() == "Team":
                team = row.find('td', class_='infobox-label').find_next_sibling('td').text.strip()
    
    if role:
        role = role.split(' ')[0];
        if role == 'Jungler':
            role = 'Jungle'
    # Check if player exists in the database
    player, created = Player.objects.get_or_create(
        name=player_name,
        defaults={
            'nationality': country_of_birth,
            'current_team': team,
            'role': role,
            'image_url': image_url,
            'league': 'Unknown',  # You might want to add league information to your scraping
            'is_active': team != 'Not found'  # Assuming the player is active by default
        }
    )
    
    # Read existing players from file
    existing_players = read_players_from_file()
    
    # If player is newly created and not in the file, add them
    if created and player_name not in existing_players:
        is_active_text = "Yes" if team != 'Not found' else "No"
        write_player_to_file(player_name, country_of_birth, team, role, image_url, is_active_text)
        return f"Player {player_name} added to the database and players.txt."
    else:
        return f"Player {player_name} already exists in the database. Information updated."


def insert_all_players_to_db():
    """Inserts all players from players.txt into the database."""
    existing_players = {player.name for player in Player.objects.all()}
    new_players = read_players_info_from_file()
    # print(new_players)
    added_count = 0
    for player_data in new_players:
        player_name = player_data[0]
        nationality = player_data[1]
        current_team = player_data[2]
        role = player_data[3]
        image_url = player_data[4]
        is_active = player_data[5]
        # player_name, nationality, current_team, role, image_url, is_active = player_data.split(';')
        print(player_name, nationality, current_team, role, image_url, is_active)
        if player_name in existing_players:
            continue
        
        Player.objects.get_or_create(
            name=player_name,
            defaults={
                'nationality': nationality,
                'current_team': current_team,
                'role': role,
                'image_url': image_url,
                'league': 'Unknown',  # Default value or parse it if available
                'is_active': is_active == "Yes"
            }
        )
        added_count += 1

    return f"Inserted {added_count} new players to the database."


# Example usage
if __name__ == "__main__":
    while True:
        print('Write a name to insert to DB. OR USE "insertdb" to add all the players from the file.')
        player_name = input("Enter player name: ")
        if player_name.lower() == "insertdb":
            print(insert_all_players_to_db())
        else:
            print(get_player_info(player_name))
