//<button class="delete-btn" data-project-id="1">Delete</button>

document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function() {
        const projectId = this.getAttribute('data-project-id');
        const confirmDelete = confirm("Are you sure you want to delete this project?");
        
        if (confirmDelete) {
            deleteProject(projectId);
        }
    });
});

function deleteProject(projectId) {
    fetch(`/delete-project/${projectId}/`, {
        method: 'DELETE', // or 'POST' if you are using a form submission
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for Django
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.ok) {
            // Optionally remove the project from the UI
            alert("Project deleted successfully!");
            // Follow-up: remove the project from the DOM or refresh the project list
        } else {
            alert("There was an issue deleting the project.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while trying to delete the project.");
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}