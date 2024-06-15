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
bank_name = "Brasil"#input("Nome do Banco: ")

host_a1 = "127.0.0.1"
port_a1 = "12346"

host_a2 = "127.0.0.1"
port_a2 = "12347"

allowed_ips = ['127.0.0.1']

# Conta de teste
users["1"] = { 'id': "1",'password': "123" }
accounts["1"] = { 'balance': 999, 'used': False}

users["1&2"] = { 'id': "1&2",'password': "123" }
accounts["1&2"] = { 'balance': 777, 'used': False}

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

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    amount = data.get('amount')
    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    user_id = session['user_id']
    accounts[user_id]['balance'] += amount
    return jsonify({'message': 'Deposit successful', 'new_balance': accounts[user_id]['balance']}), 200

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    amount = data.get('amount')
    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    user_id = session['user_id']
    if accounts[user_id]['balance'] < amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    
    accounts[user_id]['balance'] -= amount
    return jsonify({'message': 'Withdrawal successful', 'new_balance': accounts[user_id]['balance']}), 200


@app.route('/transfer', methods=['POST'])
def transfer():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    print(data)
    transfers = data.get('transfers')

    print(transfers)
    account_transfer = transfers.pop(0)
    target_username = account_transfer.get('target_username')
    account_amount = account_transfer.get('amount')

    total_amount = 0

    if account_amount == None:
        account_amount = 0

    if account_amount < 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    user_id = session['user_id']
    if accounts[user_id]['balance'] < account_amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    
    total_amount += account_amount #temp

    user_id = session.get('user_id')
    balances = consult_balances(user_id)
    print(balances)
    i = 0
    while i < len(transfers):
        amount = transfers[i]['amount']
        if amount < 0:
            return jsonify({'message': 'Invalid amount'}), 400
        if balances[i]['balance'] < amount:
            return jsonify({'message': 'Insufficient funds'}), 400
        
        print("retirando", amount) #temp

        total_amount += amount #temp
        i += 1

    target_user = users.get(target_username)
    if not target_user:
        return jsonify({'message': 'Target user does not exist'}), 404
    
    target_user_id = target_user['id']

    # accounts[user_id]['balance'] -= amount
    accounts[target_user_id]['balance'] += total_amount # temp
    
    
    print(accounts)
    return jsonify({'message': 'Transfer successful', 'new_balance': accounts[user_id]['balance']}), 200

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
Comunicação com os outros bancos
"""

# affiliates banks balances
@app.route('/ab_balance', methods=['GET'])
def ab_balances():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    balances = consult_balances(user_id)
    return  jsonify(balances), 200

def consult_balances(user_id):
    balances = []
    #response = requests.post(f'http://{host}:{port}/balance', json={'user_id': user_id})
    #data = response.json()
    #balances.append(data)
    response = requests.post(f'http://{host}:{port}/balance', json={'user_id': user_id})
    data = response.json()
    balances += data
    response = requests.post(f'http://{host}:{port}/balance', json={'user_id': user_id})
    data = response.json()
    balances += data
    return balances

@app.route('/balance', methods=['POST'])
def balance():
    # Verifica se o endereço IP da solicitação está na lista de IPs permitidos
    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403
    
    data = request.get_json()
    user_id = data.get('user_id')
    print(data)
    print(user_id)
    
    accounts_found = []
    for account_id in accounts.keys():
        if user_id == account_id or user_id in account_id.split("&"):
            accounts_found.append({'bank': bank_name, 'balance': accounts[account_id]['balance']})

    # Verifica se a conta existe
    if len(accounts_found) == 0:
        return jsonify({'message': 'User account does not exist'}), 404
    
    # Retorna o saldo da conta se a conta existir
    return jsonify(accounts_found), 200



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
    
    # Adiciona o valor na conta
    accounts[user_id]['balance'] -= amount
    return jsonify({'message': 'Amount removed to account'}), 200

if __name__ == '__main__':
    app.run(host=host, port=port)