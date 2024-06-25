document.addEventListener('DOMContentLoaded', () => {
    const accountsBalances = document.getElementById('accountsBalances');
    const logoutButton = document.getElementById('logoutButton');

    if (accountsBalances) {
        fetch('/ab_balance')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao obter os saldos dos bancos afiliados.');
                }
                return response.json();
            })
            .then(data => {
                accountsBalances.innerHTML = '';
                data.forEach(bankInfo => {
                    const bankElement = document.createElement('div');
                    bankElement.classList.add('balance-item'); // Adiciona a classe "balance"
    
                    // Ajusta o nome do banco
                    let bankName = bankInfo.bank;
                    if (bankName === "brasil") {
                        bankName = "Banco do Brasil";
                    } else if (bankName === "bradesco") {
                        bankName = "Bradesco";
                    } else if (bankName === "caixa") {
                        bankName = "Caixa Econômica Federal";
                    }
    
                    const bank = document.createElement('h3');
                    bank.textContent = bankName;
                    bankElement.appendChild(bank);
    
                    // Lógica do CPF / conta individual
                    const cpfs = document.createElement('p');
                    if (bankInfo.account_id.includes('&')) {
                        const cpf_str = bankInfo.account_id.split('&')[1].trim();
                        cpfs.textContent = `2º Titular ${cpf_str}`;
                    } else {
                        cpfs.textContent = "Conta Individual";
                    }
                    bankElement.appendChild(cpfs);
    
                    const bankBalance = document.createElement('p');
                    bankBalance.textContent = `R$ ${bankInfo.balance}`;
                    bankElement.appendChild(bankBalance);
    
                    accountsBalances.appendChild(bankElement);
                });
            })
            .catch(error => {
                console.error('Erro na atualização dos saldos dos bancos afiliados:', error);
            });
    }

    const redirectTo = (url) => {
        window.location.href = url;
    };

    logoutButton.addEventListener('click', () => {
        fetch('/logout', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            redirectTo('/login');
        });
    });

    document.getElementById('goToWithdraw').addEventListener('click', () => {
        redirectTo('/withdraw');
    });

    document.getElementById('goToDeposit').addEventListener('click', () => {
        redirectTo('/deposit');
    });

    document.getElementById('goToTransfer').addEventListener('click', () => {
        redirectTo('/transfer');
    });

    document.getElementById('goToPayment').addEventListener('click', () => {
        redirectTo('/payment');
    });
});
