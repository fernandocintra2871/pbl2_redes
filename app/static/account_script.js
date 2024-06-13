document.addEventListener('DOMContentLoaded', () => {
    const depositForm = document.getElementById('depositForm');
    const withdrawForm = document.getElementById('withdrawForm');
    const transferForm = document.getElementById('transferForm');
    const logoutButton = document.getElementById('logoutButton');
    const message = document.getElementById('message');
    const balanceText = document.getElementById('balance');
    const affiliatedBanksContainer = document.getElementById('affiliatedBanksContainer');
    const multipleTransfersCheckbox = document.getElementById('multipleTransfers');
    const extraTransfers = document.getElementById('extraTransfers');

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
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao obter os saldos dos bancos afiliados.');
                }
                return response.json();
            })
            .then(data => {
                // Limpar o contêiner e inputs antigos
                affiliatedBanksContainer.innerHTML = '';
                extraTransfers.innerHTML = '';
    
                // Adicionar novos dados
                data.forEach((bankInfo, index) => {
                    const bankElement = document.createElement('div');
                    bankElement.classList.add('balance-item');
    
                    const bankName = document.createElement('h3');
                    bankName.textContent = bankInfo.bank;
    
                    const bankBalance = document.createElement('p');
                    bankBalance.textContent = `Balance: $${bankInfo.balance}`;
    
                    bankElement.appendChild(bankName);
                    bankElement.appendChild(bankBalance);
                    affiliatedBanksContainer.appendChild(bankElement);
    
                    // Criar novo input de transferência
                    const newInput = document.createElement('input');
                    newInput.type = 'number';
                    newInput.id = `transferAmount${index + 1}`; // IDs únicos com base no índice
                    newInput.name = 'amount';
                    newInput.placeholder = `Transfer Amount from ${bankInfo.balance}`;
                    extraTransfers.appendChild(newInput);
                });
            })
            .catch(error => {
                console.error('Erro na atualização dos saldos dos bancos afiliados:', error);
                // Exibir mensagem de erro ao usuário, se necessário
            });
    };
    

    const redirectTo = (url) => {
        window.location.href = url;
    };

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
            const transfers = [{ target_username: targetUsername, amount: amount }];
    
            // Contar quantos inputs de transferência dinâmicos foram criados
            if (multipleTransfersCheckbox.checked) {
                const dynamicTransferInputs = extraTransfers.querySelectorAll('input[type="number"]');
                dynamicTransferInputs.forEach(input => {
                    const transferAmount = parseFloat(input.value);
                    if (!isNaN(transferAmount)) {
                        transfers.push({ amount: transferAmount });
                    } else {
                        transfers.push({ amount: 0 });
                    }
                });
            }
    
            fetch('/transfer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transfers })
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                updateBalance();
            })
            .catch(error => {
                console.error('Erro ao realizar a transferência:', error);
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

    if (multipleTransfersCheckbox) {
        multipleTransfersCheckbox.addEventListener('change', () => {
            if (multipleTransfersCheckbox.checked) {
                extraTransfers.style.display = 'block';
            } else {
                extraTransfers.style.display = 'none';
            }
        });
    }
});


