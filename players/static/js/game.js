document.getElementById('player-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        const playerName = document.getElementById('player-input').value;
        fetch(`/guess_player/?name=${encodeURIComponent(playerName)}`)
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('results-body');
                const errorMessage = document.getElementById('error-message');
                errorMessage.style.visibility = 'collapse';

                if (data.message === 'You have already guessed this player.') {
                    errorMessage.textContent = 'You have already guessed this player.'
                    errorMessage.style.visibility = 'visible';
                } else if (data.attributes && data.comparisons) {
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `
                        <td>${data.attributes.name}</td>
                        <td class="${data.comparisons.nationality ? 'correct' : 'incorrect'}">${data.attributes.nationality}</td>
                        <td class="${data.comparisons.current_team ? 'correct' : 'incorrect'}">${data.attributes.current_team}</td>
                        <td class="${data.comparisons.league ? 'correct' : 'incorrect'}">${data.attributes.league}</td>
                        <td class="${data.comparisons.is_active ? 'correct' : 'incorrect'}">${data.attributes.is_active ? 'Yes' : 'No'}</td>
                        <td class="${data.comparisons.role ? 'correct' : 'incorrect'}">${data.attributes.role}</td>
                    `;
                    tbody.appendChild(newRow);

                    // Check if all attributes are correct
                    if (Object.values(data.comparisons).every(value => value === true)) {
                        setTimeout(showCongratulationsPopup, 300);
                        // showCongratulationsPopup();
                    }
                } else if (data.message) {
                    errorMessage.textContent = data.message;
                    errorMessage.style.visibility = 'visible';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorMessage = document.getElementById('error-message');
                errorMessage.textContent = 'An error occurred. Please try again.';
                errorMessage.style.visibility = 'visible';
            })
            .finally(() => {
                document.getElementById('player-input').value = ''; // Clear the input field
            });
    }
});

function showCongratulationsPopup() {
    const popup = document.getElementById('congratulations-popup');
    popup.style.display = 'block';
}

document.getElementById('play-again-btn').addEventListener('click', function() {
    location.reload();
});

document.addEventListener('DOMContentLoaded', function () {
    const playerInput = document.getElementById('player-input');
    const suggestionsList = document.getElementById('suggestions-list');

    playerInput.addEventListener('input', function () {
        const query = playerInput.value.trim().toLowerCase();

        if (query.length < 1) {
            suggestionsList.style.display = 'none';
            return;
        }

        // Fetch matching players from the backend
        fetch(`/search_players?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(players => {
                suggestionsList.innerHTML = '';

                if (players.length === 0) {
                    suggestionsList.style.display = 'none';
                    return;
                }

                players.forEach(player => {
                    const item = document.createElement('div');
                    item.className = 'suggestion-item';

                    // Create an image element for the player's image
                    const img = document.createElement('img');
                    img.src = player.image_url;
                    img.alt = player.name;
                    img.style.width = '30px';
                    img.style.height = '30px';
                    img.style.marginRight = '10px';

                    // Create a span element for the player's name
                    const span = document.createElement('span');
                    span.textContent = player.name;

                    // Append the image and name to the item
                    item.appendChild(img);
                    item.appendChild(span);

                    item.addEventListener('click', () => {
                        playerInput.value = player.name;
                        playerInput.focus();
                        suggestionsList.style.display = 'none';
                        // Optionally, you can add code here to show the player details or proceed further
                    });
                    suggestionsList.appendChild(item);
                });

                suggestionsList.style.display = 'block';
            })
            .catch(error => console.error('Error fetching player data:', error));
    });

    document.addEventListener('click', (event) => {
        if (!playerInput.contains(event.target) && !suggestionsList.contains(event.target)) {
            suggestionsList.style.display = 'none';
        }
    });
});
