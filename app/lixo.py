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