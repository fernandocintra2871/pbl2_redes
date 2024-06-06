from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Simulated database
users = {}
accounts = {}

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
    return render_template('account.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users:
        return jsonify({'message': 'User already exists'}), 400
    
    user_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(password)
    users[username] = {
        'id': user_id,
        'password': hashed_password
    }
    accounts[user_id] = {
        'balance': 0
    }
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = users.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    session['user_id'] = user['id']
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
    accounts[user_id]['balance'] -= amount
    accounts[target_user_id]['balance'] += amount
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

if __name__ == '__main__':
    app.run(debug=True)
