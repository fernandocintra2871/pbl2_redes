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
                    bankElement.classList.add('balance-item');

                    const bank = document.createElement('h3');
                    bank.textContent = `${bankInfo.bank}`;
                    bankElement.appendChild(bank);

                    let cpf_str = bankInfo.account_id.replace(/&/g, ' | ');
                    const cpfs = document.createElement('p');
                    cpfs.textContent = `${cpf_str}`;
                    bankElement.appendChild(cpfs);

                    const bankBalance = document.createElement('p');
                    bankBalance.textContent = `R$${bankInfo.balance}`;
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
