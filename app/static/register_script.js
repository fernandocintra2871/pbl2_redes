document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('loginButton');
    const registerForm = document.getElementById('registerForm');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (loginButton) {
        loginButton.addEventListener('click', () => {
            redirectTo('/login');
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;
            fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
            });
        });
    }
});
