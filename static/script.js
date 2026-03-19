// This file handles client-side interactions
// The form submission is handled by HTML form action

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Script loaded successfully!');
    console.log('Tasks will be saved to the server when you submit the form.');
});

// Optional: Add confirmation before delete
document.querySelectorAll('form[action*="/delete/"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (!confirm('Are you sure you want to delete this task?')) {
            e.preventDefault();
        }
    });
});
