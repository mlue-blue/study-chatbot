// Function to send a message to the server
function sendMessage(message) {
    fetch('/api/sendMessage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Message sent:', data);
    })
    .catch((error) => {
        console.error('Error sending message:', error);
    });
}

// Function to display received messages in the UI
function displayMessage(message) {
    const chatUI = document.getElementById('chat');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatUI.appendChild(messageElement);
}