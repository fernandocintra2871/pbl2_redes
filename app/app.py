from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from time import sleep
import os
import requests
import threading

app = Flask(__name__)
app.secret_key = 'super_secret_key'

users = {}
accounts = {}

pending_undones = []

bank_name = os.environ.get("bank_name")

# Host do Banco do Brasil
host1 = os.environ.get("brasil_host")
port1 = "12345"

# Host do Bradesco
host2 = os.environ.get("bradesco_host")
port2 = "12346"

# Host da Caixa Econômica Federal
host3 = os.environ.get("caixa_host")
port3 = "12347"

host = "0.0.0.0"
if bank_name == "brasil":
    #host = host1
    port = port1
elif bank_name == "bradesco":
    #host = host2
    port = port2
elif bank_name == "caixa":
    #host = host3
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
    if bank_name == "brasil":
        bank = "Banco do Brasil"
    elif bank_name == "bradesco":
        bank = "Bradesco"
    elif bank_name == "caixa":
        bank = "Caixa Econômica Federal"
    return render_template('account.html', bank_name=bank)

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')

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
                        Registro e Login
========================================================================
"""

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
        'lock': threading.Lock()
    }

    return jsonify({'message': 'User registered successfully'}), 201

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

    if joint_account == True:
        user_id += '&' + second_holder

    target_host, target_port = get_host(bank)

    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json={'user_id': user_id, 'amount': amount}, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

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
    
    if joint_account == True:
        user_id += '&' + second_holder

    target_host, target_port = get_host(bank)
    
    try:
        response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json={'user_id': user_id, 'amount': amount}, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return jsonify({'message': 'Falha ao se comunicar com o banco destino'}), 502

    data = response.json()
    code = response.status_code
  
    return jsonify(data), code

@app.route('/ab_balance', methods=['GET'])
def ab_balances():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']

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

    return  jsonify(balances), 200

@app.route('/payment_op', methods=['POST'])
def payment_op():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    transfers = request.get_json()

    global pending_undones

    transfer_hist = []
    for transfer in transfers:
        bank = transfer['bank']
        target_host, target_port = get_host(bank)
        data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
        try:
            response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json=data, timeout=3)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            pending_undones += transfer_hist
            return jsonify({'message': 'Failure to communicate with partner bankss'}), 502
        if response.status_code != 200:
            pending_undones += transfer_hist
            return jsonify(response.json()), response.status_code
        transfer_hist.append(transfer)
   
    return jsonify({'message': 'Payment completed successfully'}), 200

#  Padrão: Saga com Coordenação de Bloqueio
@app.route('/transfer_op', methods=['POST'])
def transfer_op():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    transfers = request.get_json()
    target_transfer = transfers.pop()

    global pending_undones

    transfer_hist = []
    for transfer in transfers:
        bank = transfer['bank']
        target_host, target_port = get_host(bank)
        data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
        try:
            response = requests.post(f'http://{target_host}:{target_port}/remove_balance', json=data, timeout=3)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            pending_undones += transfer_hist
            return jsonify({'message': 'Failure to communicate with partner bankss'}), 502
        if response.status_code != 200:
            pending_undones += transfer_hist
            return jsonify(response.json()), response.status_code
        transfer_hist.append(transfer)
   
    target_bank = target_transfer['bank']
    target_host, target_port = get_host(target_bank)
    data = {'user_id': target_transfer['user_id'], 'amount': target_transfer['amount']}
    try:
        response = requests.post(f'http://{target_host}:{target_port}/add_balance', json=data, timeout=3)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        pending_undones += transfer_hist
        return jsonify({'message': 'Failure to communicate with partner banks'}), 502
    if response.status_code != 200:
        pending_undones += transfer_hist
        return jsonify(response.json()), response.status_code

    return jsonify({'message': 'Transfer completed successfully'}), 200

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

@app.route('/add_balance', methods=['POST'])
def add_balance():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    accounts[user_id]['lock'].acquire(blocking=True)
    accounts[user_id]['balance'] += data['amount']
    accounts[user_id]['lock'].release()

    return jsonify({'message': 'Amount added to account'}), 200

@app.route('/remove_balance', methods=['POST'])
def remove_balance():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if user_id not in accounts:
        return jsonify({'message': 'User account does not exist'}), 404
    
    accounts[user_id]['lock'].acquire(blocking=True)
    if accounts[user_id]['balance'] < data['amount']:
        accounts[user_id]['lock'].release()
        return jsonify({'message': 'Insufficient funds'}), 400
    accounts[user_id]['balance'] -= data['amount']
    accounts[user_id]['lock'].release()
    
    return jsonify({'message': 'Amount removed to account'}), 200

@app.route('/balances/<string:user_id>', methods=['GET'])
def balances(user_id):
    accounts_found = []
    for account_id in accounts.keys():
        if user_id == account_id or user_id in account_id.split("&"):
            accounts_found.append({'account_id': account_id, 'bank': bank_name, 'balance': accounts[account_id]['balance']})

    if len(accounts_found) == 0:
        return jsonify({'message': 'User account does not exist'}), 404
    
    return jsonify(accounts_found), 200

"""
========================================================================
                            Threds
========================================================================
"""

def undo_transfers():
    while True:
        sleep(0.1)
        if len(pending_undones) > 0:
            transfer = pending_undones.pop(0)
            bank = transfer['bank']
            target_host, target_port = get_host(bank)
            data = {'user_id': transfer['user_id'], 'amount': transfer['amount']}
            try:
                response = requests.post(f'http://{target_host}:{target_port}/add_balance', json=data, timeout=3)
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                pending_undones.append(transfer)

"""
========================================================================
                            Main
========================================================================
"""

if __name__ == '__main__':
    threading.Thread(target=undo_transfers, daemon=True).start()
    app.run(host=host, port=port)