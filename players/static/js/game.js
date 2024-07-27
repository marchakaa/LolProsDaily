document.addEventListener('DOMContentLoaded', function() {
    let mode = '';

    if (document.getElementById('home-page')) {
        mode = 'home';
    } else if (document.getElementById('practice-page')) {
        mode = 'practice';
    }

    const playerInput = document.getElementById('player-input');

    // Listen for Enter key press
    playerInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent form submission if applicable
            submitGuess(mode);
        }
    });

    // Optional: If you still want a button (for accessibility)
    document.getElementById('play-again-btn').addEventListener('click', function() {
        location.reload();
    });
});

function submitGuess(mode) {
    const playerName = document.getElementById('player-input').value;

    // Determine the endpoint based on the mode
    let url = '';
    if (mode === 'home') {
        url = `/guess_player/?name=${encodeURIComponent(playerName)}&mode=home`;
    } else if (mode === 'practice') {
        url = `/guess_player/?name=${encodeURIComponent(playerName)}&mode=practice`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('results-body');
            const errorMessage = document.getElementById('error-message');
            errorMessage.style.visibility = 'collapse';

            if (data.message === 'You have already guessed this player.') {
                errorMessage.textContent = 'You have already guessed this player.';
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

function showCongratulationsPopup() {
    const popup = document.getElementById('congratulations-popup');
    popup.style.display = 'block';
}
