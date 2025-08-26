// This file contains JavaScript for client-side functionality.
// You can add event listeners, AJAX calls, and other interactive features here.

document.addEventListener('DOMContentLoaded', function() {
    // Example: Handle profile picture upload
    const profilePicInput = document.getElementById('profile-pic-input');
    const profilePicPreview = document.getElementById('profile-pic-preview');

    if (profilePicInput) {
        profilePicInput.addEventListener('change', function() {
            const file = profilePicInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    profilePicPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Example: Simple messaging system (to be expanded)
    const messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const messageInput = document.getElementById('message-input');
            const message = messageInput.value;
            if (message) {
                // Send message via WebSocket or AJAX
                console.log('Message sent:', message);
                messageInput.value = ''; // Clear input
            }
        });
    }
});