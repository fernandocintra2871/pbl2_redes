from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from time import sleep
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Simulated database
users = {}
accounts = {}


host = "127.0.0.1"
port = input("Porta: ")
bank_name = input("Nome do Banco: ")

host_a1 = "127.0.0.1"
port_a1 = "12346"

host_a2 = "127.0.0.1"
port_a2 = "12347"


# Conta de teste
users["1"] = { 'id': "1",'password': "123" }
accounts["1"] = { 'balance': 999, 'used': False}


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
    target_username = data.get('target_username')
    amount = data.get('amount')
    
    if amount <= 0:
        return jsonify({'message': 'Invalid amount'}), 400
    
    target_user = users.get(target_username)
    if not target_user:
        return jsonify({'message': 'Target user does not exist'}), 404
    
    user_id = session['user_id']
    if accounts[user_id]['balance'] < amount:
        return jsonify({'message': 'Insufficient funds'}), 400
    
    target_user_id = target_user['id']

    """
    c = 0
    while accounts[user_id]['used'] and accounts[target_user_id]['used']:
        if c > 1000000000:
            return jsonify({'message': 'Target user does not exist'}), 423
        c += 1
   
    accounts[user_id]['used'] = True
    accounts[target_user_id]['used'] = True
    """

    accounts[user_id]['balance'] -= amount
    accounts[target_user_id]['balance'] += amount
    
    #accounts[user_id]['used'] = False
    #accounts[target_user_id]['used'] = False
    
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
    response = requests.post(f'http://{host_a1}:{port_a1}/balance', json={'user_id': user_id})
    data = response.json()
    return  jsonify(data), 200

@app.route('/balance', methods=['POST'])
def balance():
     # Verifica se o endereço IP da solicitação está na lista de IPs permitidos
    allowed_ips = ['127.0.0.1'] 
    client_ip = request.remote_addr
    if client_ip not in allowed_ips:
        return jsonify({'message': 'Forbidden'}), 403
    data = request.get_json()
    user_id = data.get('user_id')
    print(data)
    print(user_id)
    return jsonify({'bank': bank_name, 'balance': accounts[user_id]['balance']}), 200

if __name__ == '__main__':
    app.run(host=host, port=port)