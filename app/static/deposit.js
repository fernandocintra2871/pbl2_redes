document.addEventListener('DOMContentLoaded', () => {
    const depositForm = document.getElementById('depositForm');
    const jointAccountCheckbox = document.getElementById('depositJointAccount');
    const message = document.getElementById('message');

    const showMessage = (msg) => {
        message.textContent = msg;
    };

    const redirectTo = (url) => {
        window.location.href = url;
    };

    if (depositForm) {
        depositForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const bank = document.getElementById('depositBankSelection').value;
            const joint_account = document.getElementById('depositJointAccount').checked;
            const second_holder = document.getElementById('depositSecondHolder').value;
            const amount = parseFloat(document.getElementById('depositAmount').value);

            const formData = {
                bank: bank,
                joint_account: joint_account,
                second_holder: second_holder,
                amount: amount
            }
            
            fetch('/deposit_op', {
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
                document.getElementById('depositSecondHolder').style.display = 'block';
                document.getElementById('depositSecondHolder').setAttribute('required');
            } else {
                document.getElementById('depositSecondHolder').style.display = 'none';
                document.getElementById('depositSecondHolder').removeAttribute('required');
                document.getElementById('depositSecondHolder').value = '';
            }
        });
    }
   
    document.getElementById('goBack').addEventListener('click', () => {
        redirectTo('/');
    });
});
