from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from time import sleep
import os
import requests
import threading

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Dicionários para armazenar usuários e contas
users = {}
accounts = {}

# Lista para armazenar transferências pendentes
pending_undones = []

# Obter o nome do banco a partir das variáveis de ambiente
bank_name = os.environ.get("bank_name")

# Host dos bancos
host1 = os.environ.get("brasil_host")
port1 = "12345"
host2 = os.environ.get("bradesco_host")
port2 = "12346"
host3 = os.environ.get("caixa_host")
port3 = "12347"

# Definir o host padrão como 0.0.0.0
host = "0.0.0.0"
if bank_name == "brasil":
    port = port1
elif bank_name == "bradesco":
    port = port2
elif bank_name == "caixa":
    port = port3

# Conta de teste
users["06440742051"] = { 'id': "06440742051",'password': "123" }
accounts["06440742051"] = { 'balance': 1000, 'lock': threading.Lock() }

users["06440742051&27574742006"] = { 'id': "06440742051&27574742006",'password': "123" }
accounts["06440742051&27574742006"] = { 'balance': 500, 'lock': threading.Lock() }

users["06440742051&30739886029"] = { 'id': "06440742051&30739886029",'password': "123" }
accounts["06440742051&30739886029"] = { 'balance': 200, 'lock': threading.Lock() }

users["27574742006"] = { 'id': "27574742006",'password': "123" }
accounts["27574742006"] = { 'balance': 0, 'lock': threading.Lock()}


"""
========================================================================
                    Rotas das Paginas do Sistema
========================================================================
"""

# Rota principal, redireciona para a página de login se o usuário não estiver autenticado
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('account'))
    return redirect(url_for('login'))

# Rota para a página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Rota para a página de registro
@app.route('/register')
def register():
    return render_template('register.html')

# Rotas para páginas da conta
@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Altera o nome do banco exibido na pagina de acordo com o banco que foi instanciado
    if bank_name == "brasil":
        bank = "Banco do Brasil"
    elif bank_name == "bradesco":
        bank = "Bradesco"
    elif bank_name == "caixa":
        bank = "Caixa Econômica Federal"
    return render_template('account.html', bank_name=bank)

# Rotas para páginas de operações
@app.route('/withdraw')
def withdraw():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('withdraw.html')

@app.route('/deposit')
def deposit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('transfer.html')

@app.route('/payment')
def payment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('payment.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200


"""
========================================================================
                        Registro e Login
========================================================================
"""

# Rota para registrar um novo usuário
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users:
        return jsonify({'message': 'User already exists'}), 400
    
    users[username] = {
        'id': username,
        'password': password
    }
    accounts[username] = {
        'balance': 0,
        'used': False,
        'lock': threading.Lock() # Trava da conta, o saldo da conta é travado sempre que o saldo vai ser modificado
    }

    return jsonify({'message': 'User registered successfully'}), 201

# Rota para autenticar um usuário
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = None
    for user_id in users.keys():
        if username == user_id or username in user_id.split("&"):
            user = users[user_id]
            break

    if not user or not user['password'] == password:
        return jsonify({'message': 'Invalid username or password'}), 401
    
    session['user_id'] = username
    return jsonify({'message': 'Login successful'}), 200

"""
========================================================================
                        Operações
========================================================================
"""

# Rota para realizar depósito
@app.route('/deposit_op', methods=['POST'])
def deposit_op():
    data = request.get_json()

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    bank = data['bank']
    joint_account = data['joint_account']
    second_holder = data['second_holder']
    amount = data['amount']

    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    #  Verifica se a conta é conjunta, se for o ID será o ID do usuario + ID do 2º titular
    if joint_account == True:
        user_id += '&' + second_holder

    target_host, target_port = get_host(bank)

    # Tenta enviar uma requisição para rota /add_balance do banco da operação
    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json={'user_id': user_id, 'amount': amount}, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

# Rota para realizar saque
@app.route('/withdraw_op', methods=['POST'])
def withdraw_op():
    data = request.get_json()

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    bank = data['bank']
    joint_account = data['joint_account']
    second_holder = data['second_holder']
    amount = data['amount']

    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    #  Verifica se a conta é conjunta, se for o ID será o ID do usuario + ID do 2º titular
    if joint_account == True:
        user_id += '&' + second_holder

    target_host, target_port = get_host(bank)
    
    # Tenta enviar uma requisição para rota /remove_balance do banco da operação
    try:
        response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json={'user_id': user_id, 'amount': amount}, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

# Rota para obter saldos de todas as contas bancárias do usuario autenticado
@app.route('/ab_balance', methods=['GET'])
def ab_balances():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']

    # Tenta obeter os saldos das contas do usuario em cada um dos tres bancos
    balances = []
    try:
        response = requests.get(f'http://{host1}:{port1}/balances/{user_id}', timeout=3)
        if response.status_code == 200:
            data = response.json()
            balances += data
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        pass

    try:
        response = requests.get(f'http://{host2}:{port2}/balances/{user_id}', timeout=3)
        if response.status_code == 200:
            data = response.json()
            balances += data
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        pass

    try:
        response = requests.get(f'http://{host3}:{port3}/balances/{user_id}', timeout=3)
        if response.status_code == 200:
            data = response.json()
            balances += data
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        pass

    # Retorna uma lista com os saldos das contas encontradas
    return  jsonify(balances), 200

# Rota para realizar pagamento
@app.route('/payment_op', methods=['POST'])
def payment_op():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    transfers = request.get_json()

    global pending_undones # Lista global de operações a serem desfeitas

    transfer_hist = [] # Log das operações envolvidas na transação que já foram realizadas
    for transfer in transfers:
        bank = transfer['bank']
        target_host, target_port = get_host(bank)
        data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
        # Tenta enviar uma requisição para rota /remove_balance do banco da operação para remover o respectivo valor da conta
        try:
            response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json=data, timeout=3)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            # Caso o banco perca a comunicação o log das operações já realizadas é adicionado a lista de operações pendentes para serem desfeitas
            pending_undones += transfer_hist
            return jsonify({'message': 'Failure to communicate with partner bankss'}), 502
        if response.status_code != 200:
            # Caso a operação seja invalida (ex: saldo insuficiente) o log das operações já realizadas é adicionado a lista de operações pendentes para serem desfeitas
            pending_undones += transfer_hist
            return jsonify(response.json()), response.status_code
        transfer_hist.append(transfer) # Adicionma a operação que acabou de ser realizada ao log de operações já realizadas
   
    return jsonify({'message': 'Payment completed successfully'}), 200

# Rota para realizar trasnferencia
@app.route('/transfer_op', methods=['POST'])
def transfer_op():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    transfers = request.get_json()
    target_transfer = transfers.pop()

    global pending_undones # Lista global de operações a serem desfeitas

    transfer_hist = [] # Log das operações envolvidas na transação que já foram realizadas
    for transfer in transfers:
        bank = transfer['bank']
        target_host, target_port = get_host(bank)
        data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
        # Tenta enviar uma requisição para rota /remove_balance do banco da operação para remover o respectivo valor da conta
        try:
            response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json=data, timeout=3)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
             # Caso o banco perca a comunicação o log das operações já realizadas é adicionado a lista de operações pendentes para serem desfeitas
            pending_undones += transfer_hist
            return jsonify({'message': 'Failure to communicate with partner bankss'}), 502
        if response.status_code != 200:
            # Caso a operação seja invalida (ex: saldo insuficiente) o log das operações já realizadas é adicionado a lista de operações pendentes para serem desfeitas
            pending_undones += transfer_hist
            return jsonify(response.json()), response.status_code
        transfer_hist.append(transfer) # Adicionma a operação que acabou de ser realizada ao log de operações já realizadas
   
   # Pega o alvo da transferencia (sempre o ultimo item da lista "transfers")
    target_bank = target_transfer['bank']
    target_host, target_port = get_host(target_bank)
    data = {'user_id': target_transfer['user_id'], 'amount': target_transfer['amount']}
    # Tenta enviar uma requisição para rota /aa_balance do banco da operação para adicionar o respectivo valor da conta
    # O "amount" dessa operação já é a soma dos valores das operações anteriores
    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json=data, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        pending_undones += transfer_hist
        return jsonify({'message': 'Failure to communicate with partner banks'}), 502
    if response.status_code != 200:
        pending_undones += transfer_hist
        return jsonify(response.json()), response.status_code

    return jsonify({'message': 'Transfer completed successfully'}), 200

# Função que retorna a HOST e a PORT de cada banco de acordo com os valores das variaveis de ambiente
def get_host(bank):
    if bank == 'brasil':
        target_host = host1
        target_port = port1
    elif bank == 'bradesco':
        target_host = host2
        target_port = port2
    elif bank == 'caixa':
        target_host = host3
        target_port = port3

    return target_host, target_port

"""
========================================================================
                        Requisições Entre Bancos
========================================================================
"""

# Rota para adicionar um valor a uma conta no banco
@app.route('/add_balance', methods=['POST'])
def add_balance():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    # Tenta obter a trava (lock()) do saldo da conta, 
    # caso consiga, o a execução prossegue, 
    # caso não, a execução entre em espera até que a trava seja liberada
    accounts[user_id]['lock'].acquire(blocking=True)
    accounts[user_id]['balance'] += data['amount']
    accounts[user_id]['lock'].release() # libera a trava do saldo da conta

    return jsonify({'message': 'Amount added to account'}), 200

# Rota para remover um valor de uma conta no banco
@app.route('/remove_balance', methods=['POST'])
def remove_balance():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    # Tenta obter a trava (lock()) do saldo da conta, 
    # caso consiga, o a execução prossegue, 
    # caso não, a execução entre em espera até que a trava seja liberada
    accounts[user_id]['lock'].acquire(blocking=True)
    if accounts[user_id]['balance'] < data['amount']:
        accounts[user_id]['lock'].release()
        return jsonify({'message': 'Insufficient funds'}), 400
    accounts[user_id]['balance'] -= data['amount']
    accounts[user_id]['lock'].release()  # libera a trava do saldo da conta
    
    return jsonify({'message': 'Amount removed to account'}), 200

# Rota para obter o saldo de uma conta no banco
@app.route('/balances/<string:user_id>', methods=['GET'])
def balances(user_id):
    accounts_found = []
    for account_id in accounts.keys():
        if user_id == account_id or user_id in account_id.split("&"): # Verifica se o ID (CPF) faz parte do ID de alguma conta conjunta
            accounts_found.append({'account_id': account_id, 'bank': bank_name, 'balance': accounts[account_id]['balance']})

    if len(accounts_found) == 0:
        return jsonify({'message': 'User account does not exist'}), 404
    
    return jsonify(accounts_found), 200

"""
========================================================================
                            Threds
========================================================================
"""

# Thred que é encubida de desfazer as operações presentes em "peding_undones"
def undo_transfers():
    while True:
        sleep(0.1) # Atraso para que seja possivel o servidor receber chamadas da API
        if len(pending_undones) > 0:
            transfer = pending_undones.pop(0)
            bank = transfer['bank']
            target_host, target_port = get_host(bank)
            data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
            try:
                response = requests.post(f'http://{target_host}:{target_port}/add_balance', json=data, timeout=3)
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                pending_undones.append(transfer) # Se não for possivel desfazer a operação ela é novamente adicionada na lista

"""
========================================================================
                            Main
========================================================================
"""

if __name__ == '__main__':
    threading.Thread(target=undo_transfers, daemon=True).start()
    app.run(host=host, port=port)