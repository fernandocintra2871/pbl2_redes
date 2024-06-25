document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('loginButton');
    const registerForm = document.getElementById('registerForm');
    const message = document.getElementById('message');
    const registerJointAccountCheckbox = document.getElementById('registerJointAccount');

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
            let username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;

            if (registerJointAccountCheckbox.checked) {
                const username2 = document.getElementById('registerUsername2').value;
                username = `${username}&${username2}`;
            }

            fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                setTimeout(() => {redirectTo('/login');}, 2000);
            });
        });
    }

    if (registerJointAccountCheckbox) {
        registerJointAccountCheckbox.addEventListener('change', () => {
            if (registerJointAccountCheckbox.checked) {
                document.getElementById('registerUsername2').style.display = 'block';
                document.getElementById('registerUsername2').setAttribute('required');
            } else {
                document.getElementById('registerUsername2').style.display = 'none';
                document.getElementById('registerUsername2').removeAttribute('required');
                document.getElementById('registerUsername2').value = '';
            }
        });
    }

});