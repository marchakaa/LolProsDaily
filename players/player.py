import requests
from bs4 import BeautifulSoup

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
    
    # Format and return the result
    return f"""Name: {player_name}
Country of Birth: {country_of_birth}
Role: {role}
Team: {team}
Image URL: {image_url}"""

# Example usage
while True:
    player_name = input("Enter player name: ")
    print(get_player_info(player_name))