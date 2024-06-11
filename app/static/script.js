document.addEventListener('DOMContentLoaded', () => {
    const registerButton = document.getElementById('registerButton');
    const loginButton = document.getElementById('loginButton');
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const depositForm = document.getElementById('depositForm');
    const transferForm = document.getElementById('transferForm');
    const logoutButton = document.getElementById('logoutButton');
    const message = document.getElementById('message');
    const balanceText = document.getElementById('balance');
    const abBalanceText1 = document.getElementById('abBalance1');
    const abNameText1 = document.getElementById('abName1');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const updateBalance = () => {
        fetch('/account_balance')
            .then(response => response.json())
            .then(data => {
                if (data.balance !== undefined) {
                    balanceText.textContent = `Balance: $${data.balance}`;
                }
            });
    };

    const updateAbBalance = () => {
        fetch('/ab_balance')
            .then(response => response.json())
            .then(data => {
                if (data.balance !== undefined) {
                    abBalanceText1.textContent = `Balance: $${data.balance}`;
                    abNameText1.textContent = `${data.bank}`;
                }
            });
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (registerButton) {
        registerButton.addEventListener('click', () => {
            redirectTo('/register');
        });
    }

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

    if (depositForm) {
        depositForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const amount = parseFloat(document.getElementById('depositAmount').value);
            fetch('/deposit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                updateBalance();
            });
        });
    }

    if (withdrawForm) {
        withdrawForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const amount = parseFloat(document.getElementById('withdrawAmount').value);
            fetch('/withdraw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                updateBalance();
            });
        });
    }
    

    if (transferForm) {
        transferForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const targetUsername = document.getElementById('transferUsername').value;
            const amount = parseFloat(document.getElementById('transferAmount').value);
            const targetBank = document.getElementById('transferBank').value;
            fetch('/transfer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_username: targetUsername, amount, target_bank: targetBank })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                updateBalance();
            });
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            fetch('/logout', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                redirectTo('/login');
            });
        });
    }

    if (balanceText) {
        updateBalance();
        updateAbBalance();
    }
});
