console.log(123)
function rotateCard(event, card) {
    const cardRect = card.getBoundingClientRect();
    const centerX = cardRect.left + cardRect.width / 2;
    const centerY = cardRect.top + cardRect.height / 2;
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    const rotateX = (mouseY - centerY) / 20; // Adjust sensitivity
    const rotateY = (centerX - mouseX) / 20; // Adjust sensitivity

    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
}

function resetCard(card) {
    card.style.transform = 'rotateX(0) rotateY(0)';
}
