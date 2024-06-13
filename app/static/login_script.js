document.addEventListener('DOMContentLoaded', () => {
    const registerButton = document.getElementById('registerButton');
    const loginForm = document.getElementById('loginForm');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (registerButton) {
        registerButton.addEventListener('click', () => {
            redirectTo('/register');
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                if (data.message === 'Login successful') {
                    redirectTo('/account');
                }
            });
        });
    }
});
