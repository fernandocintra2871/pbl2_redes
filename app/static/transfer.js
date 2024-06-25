document.addEventListener('DOMContentLoaded', () => {
    const transferForm = document.getElementById('transferForm');
    const transferJointAccountCheckbox = document.getElementById('transferJointAccount');
    const transferAmounts = document.getElementById('transferAmounts');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (transferForm) {
        transferForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const bank = document.getElementById('bankSelection').value;
            const joint_account = document.getElementById('transferJointAccount').checked;
            const target1 = document.getElementById('transferTarget1').value;
            const target2 = document.getElementById('transferTarget2').value;
            
            const transfers = [];
            let total_amount = 0;
            const dynamicTransferInputs = transferAmounts.querySelectorAll('input[type="number"]');
            dynamicTransferInputs.forEach(input => {
                let parts = input.name.split('|');
                const transferBank = parts[0];
                const transferID = parts[1];
                const transferAmount = parseFloat(input.value);
                if (!isNaN(transferAmount)) {
                    transfers.push({ user_id: transferID, bank: transferBank, operation:'subtraction',  amount:  transferAmount });
                    total_amount += transferAmount;
                }
            });

            const target = joint_account ? `${target1}&${target2}` : target1;
            transfers.push({ bank: bank, user_id: target, operation: 'addition', amount: total_amount });

            if (transfers.length > 1){
                fetch('/transfer_op', {
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
                    console.error('Erro ao realizar a transferência:', error);
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
                    // Ajusta o nome do banco
                    let bankName = bankInfo.bank;
                    if (bankName === "brasil") {
                        bankName = "Banco do Brasil";
                    } else if (bankName === "bradesco") {
                        bankName = "Bradesco";
                    } else if (bankName === "caixa") {
                        bankName = "Caixa Econômica Federal";
                    }
    
                    // Ajusta o tipo de conta
                    let accountType = "";
                    if (bankInfo.account_id.includes('&')) {
                        const cpf_str = bankInfo.account_id.split('&')[1].trim();
                        accountType = ` (2º titular ${cpf_str})`;
                    } else {
                        accountType = " (Individual)";
                    }
    
                    // Cria o input
                    const newInput = document.createElement('input');
                    newInput.type = 'number';
                    newInput.id = `transferAmount${index + 1}`;
                    newInput.name = `${bankInfo.bank}|${bankInfo.account_id}`;
                    newInput.step = "0.01";
                    newInput.placeholder = `${bankName}${accountType}`;
                    
                    // Adiciona o input ao elemento transferAmounts
                    transferAmounts.appendChild(newInput);
                });
            })
            .catch(error => {
                console.error('Erro na atualização dos saldos dos bancos afiliados:', error);
            });
    }
    

    if (transferJointAccountCheckbox) {
        transferJointAccountCheckbox.addEventListener('change', () => {
            if (transferJointAccountCheckbox.checked) {
                document.getElementById('transferTarget2').style.display = 'block';
                document.getElementById('transferTarget2').setAttribute('required');
            } else {
                document.getElementById('transferTarget2').style.display = 'none';
                document.getElementById('transferTarget2').removeAttribute('required');
                document.getElementById('transferTarget2').value = '';
            }
        });
    }

    document.getElementById('goBack').addEventListener('click', () => {
        redirectTo('/');
    });


});
