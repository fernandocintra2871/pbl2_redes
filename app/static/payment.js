document.addEventListener('DOMContentLoaded', () => {
    const paymentForm = document.getElementById('paymentForm');
    const transferAmounts = document.getElementById('transferAmounts');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (paymentForm) {
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const payment_target = document.getElementById('paymentTarget').value;
            
            const transfers = [];

            const dynamicTransferInputs = transferAmounts.querySelectorAll('input[type="number"]');
            dynamicTransferInputs.forEach(input => {
                let parts = input.name.split('|');
                const transferBank = parts[0];
                const transferID = parts[1];
                const transferAmount = parseFloat(input.value);
                if (!isNaN(transferAmount)) {
                    transfers.push({ user_id: transferID, bank: transferBank, operation:'subtraction',  amount:  transferAmount });
                }
            });

            if (transfers.length > 1){
                fetch('/payment_op', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(transfers)
                })
                .then(response => response.json())
                .then(data => {
                    showMessage(data.message);
                    setTimeout(() => {
                        redirectTo('/');
                    }, 2000); // Redirecionar para a página principal após 2 segundos
                })
                .catch(error => {
                    console.error('Erro ao realizar o pagamento:', error);
                });
            } else {
                showMessage('Nenhuma transferência válida encontrada.');
            }
        });
    }

    if (transferAmounts) {
        fetch('/ab_balance')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao obter os saldos dos bancos afiliados.');
                }
                return response.json();
            })
            .then(data => {
                transferAmounts.innerHTML = '';
                data.forEach((bankInfo, index) => {
                    const newInput = document.createElement('input');
                    newInput.type = 'number';
                    newInput.id = `transferAmount${index + 1}`;
                    newInput.name = `${bankInfo.bank}|${bankInfo.account_id}`;
                    let cpf_str = bankInfo.account_id.replace(/&/g, ' | ');
                    newInput.placeholder = `${bankInfo.bank}: ${cpf_str}`;
                    transferAmounts.appendChild(newInput);
                });
            })
            .catch(error => {
                console.error('Erro na atualização dos saldos dos bancos afiliados:', error);
            });
    }

    document.getElementById('goBack').addEventListener('click', () => {
        redirectTo('/');
    });

});
