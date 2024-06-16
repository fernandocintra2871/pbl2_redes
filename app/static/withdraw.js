document.addEventListener('DOMContentLoaded', () => {
    const withdrawForm = document.getElementById('withdrawForm');
    const jointAccountCheckbox = document.getElementById('withdrawJointAccount');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (withdrawForm) {
        withdrawForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const bank = document.getElementById('withdrawBankSelection').value;
            const joint_account = document.getElementById('withdrawJointAccount').checked;
            const second_holder = document.getElementById('withdrawSecondHolder').value;
            const amount = parseFloat(document.getElementById('withdrawAmount').value);

            const formData = {
                bank: bank,
                joint_account: joint_account,
                second_holder: second_holder,
                amount: amount
            }

            fetch('/withdraw_op', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                showMessage(data.message);
                setTimeout(() => {
                    redirectTo('/');
                }, 2000); // Redirecionar para a página principal após 2 segundos
            });
        });
    }

    if (jointAccountCheckbox) {
        jointAccountCheckbox.addEventListener('change', () => {
            if (jointAccountCheckbox.checked) {
                document.getElementById('withdrawSecondHolder').style.display = 'block';
                document.getElementById('withdrawSecondHolder').setAttribute('required', true);
            } else {
                document.getElementById('withdrawSecondHolder').style.display = 'none';
                document.getElementById('withdrawSecondHolder').removeAttribute('required');
                document.getElementById('withdrawSecondHolder').value = '';
            }
        });
    }

    document.getElementById('goBack').addEventListener('click', () => {
        redirectTo('/');
    });
});
