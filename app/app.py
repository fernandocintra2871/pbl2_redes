from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from time import sleep
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Simulated database
users = {}
accounts = {}


host = "127.0.0.1"
port = "12345"#input("Porta: ")
bank_name = "brasil"#input("Nome do Banco: ")

# Host do Banco do Brasil
host1 = "127.0.0.1"
port1 = "12345"

# Host do Bradesco
host2 = "127.0.0.1"
port2 = "12346"

# Host da Caixa Econômica Federal
host3 = "127.0.0.1"
port3 = "12347"

allowed_ips = ['127.0.0.1']

# Conta de teste
users["1"] = { 'id': "1",'password': "123" }
accounts["1"] = { 'balance': 1000, 'used': False }

users["1&2"] = { 'id': "1&2",'password': "123" }
accounts["1&2"] = { 'balance': 500, 'used': False }

users["2"] = { 'id': "2",'password': "123" }
accounts["2"] = { 'balance': 0, 'used': False}


@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('account'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('account.html', bank_name=bank_name)

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

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
        'used': False
    }

    print(users, accounts)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if not user or not user['password'] == password:
        return jsonify({'message': 'Invalid username or password'}), 401
    
    session['user_id'] = user['id']
    print(session)
    return jsonify({'message': 'Login successful'}), 200


@app.route('/account_balance', methods=['GET'])
def account_balance():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    return jsonify({'balance': accounts[user_id]['balance']}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

"""
========================================================================
                    Comunicação entre os bancos
========================================================================
"""

@app.route('/deposit_op', methods=['POST'])
def deposit_op():
    data = request.get_json()

    print("Deposito")
    print(data)

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    bank = data['bank']
    joint_account = data['joint_account']
    second_holder = data['second_holder']
    amount = data['amount']

    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400

    if joint_account == True:
        user_id += '&' + second_holder

    if bank == 'brasil':
        target_host = host1
        target_port = port1
    elif bank == 'bradesco':
        target_host = host2
        target_port = port2
    elif bank == 'caixa':
        target_host = host3
        target_port = port3

    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json={'user_id': user_id, 'amount': amount})
    except requests.exceptions.ConnectionError:
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

@app.route('/withdraw_op', methods=['POST'])
def withdraw_op():
    data = request.get_json()

    print("Saque")
    print(data)

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    bank = data['bank']
    joint_account = data['joint_account']
    second_holder = data['second_holder']
    amount = data['amount']

    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    if joint_account == True:
        user_id += '&' + second_holder

    if bank == 'brasil':
        target_host = host1
        target_port = port1
    elif bank == 'bradesco':
        target_host = host2
        target_port = port2
    elif bank == 'caixa':
        target_host = host3
        target_port = port3
    
    try:
        response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json={'user_id': user_id, 'amount': amount})
    except requests.exceptions.ConnectionError:
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

@app.route('/transfer_op', methods=['POST'])
def transfer_op():
    data = request.get_json()

    print("Trasnferencia")
    print(data)

    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    target_bank = data['bank']
    joint_account = data['joint_account']
    if joint_account:
        target = data['target1'] + '&' + data['target2']
    else:
        target = data['target1']
    transfers = data['transfers']

    total_amount = 0
    for transfer in transfers:
        bank = transfer['bank']
        user_id = transfer['user_id']
        amount = transfer['amount']

        if bank == 'brasil':
            target_host = host1
            target_port = port1
        elif bank == 'bradesco':
            target_host = host2
            target_port = port2
        elif bank == 'caixa':
            target_host = host3
            target_port = port3
        
        try:
            response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json={'user_id': user_id, 'amount': amount})
        except requests.exceptions.ConnectionError:
            print('Deu b.o')

        total_amount += amount

    if target_bank == 'brasil':
        target_host = host1
        target_port = port1
    elif target_bank == 'bradesco':
        target_host = host2
        target_port = port2
    elif target_bank == 'caixa':
        target_host = host3
        target_port = port3

    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json={'user_id': target, 'amount': total_amount})
    except requests.exceptions.ConnectionError:
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    print(response.json())
    return jsonify({'message': 'Trasnferencia realizada com sucesso!'}), 200

# affiliates banks balances
@app.route('/ab_balance', methods=['GET'])
def ab_balances():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    balances = consult_balances(user_id)
    #print("balances")
    #print(balances)
    return  jsonify(balances), 200

def consult_balances(user_id):
    balances = []
    response = requests.get(f'http://{host}:{port}/balances/{user_id}')
    data = response.json()
    balances += data
    response = requests.get(f'http://{host}:{port}/balances/{user_id}')
    data = response.json()
    balances += data
    response = requests.get(f'http://{host}:{port}/balances/{user_id}')
    data = response.json()
    balances += data
    return balances

@app.route('/balances/<string:user_id>', methods=['GET'])
def balances(user_id):
    # Verifica se o endereço IP da solicitação está na lista de IPs permitidos
    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403
    
    accounts_found = []
    for account_id in accounts.keys():
        if user_id == account_id or user_id in account_id.split("&"):
            accounts_found.append({'account_id': account_id, 'bank': bank_name, 'balance': accounts[account_id]['balance']})

    # Verifica se a conta existe
    if len(accounts_found) == 0:
        return jsonify({'message': 'User account does not exist'}), 404
    
    # Retorna o saldo da conta se a conta existir
    return jsonify(accounts_found), 200

@app.route('/balance/<string:user_id>', methods=['GET'])
def balance(user_id):

    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403

    if user_id in accounts.keys():
        return jsonify({'balance': accounts[user_id]['balance']}), 200
    else:
        return jsonify({'message': 'User account does not exist'}), 404


@app.route('/add_balance', methods=['POST'])
def add_balance():
    # Verifica se o endereço IP da solicitação está na lista de IPs permitidos
    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    # Verifica se a conta existe
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    # Adiciona o valor na conta
    accounts[user_id]['balance'] += amount
    return jsonify({'message': 'Amount added to account'}), 200

@app.route('/remove_balance', methods=['POST'])
def remove_balance():
    # Verifica se o endereço IP da solicitação está na lista de IPs permitidos
    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')
    
    # Verifica se a conta existe
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    if accounts[user_id]['balance'] < amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    
    accounts[user_id]['balance'] -= amount
    return jsonify({'message': 'Amount removed to account'}), 200

if __name__ == '__main__':
    app.run(host=host, port=port)