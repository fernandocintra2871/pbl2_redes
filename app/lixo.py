
@app.route('/prepare', methods=['POST'])
def prepare():
    data = request.json

    user_id = data['user_id']
    if data['operation'] == 'subtraction':
        if data['amount'] > 0 and data['amount'] <= accounts[user_id]['balance']:
            locked = accounts[user_id]['lock'].acquire(blocking=False)
            if not locked:
                return jsonify({'vote': 'abort'})
            accounts[user_id] -= data['amount']
            accounts[user_id]['lock'].release()
        else:
            return jsonify({'vote': 'abort'})
        
    transaction_id = data['transaction_id ']
    transactions[transaction_id] = {'prepared': True,'transaction_data': data, 'decision_received': threading.Event()}
    return jsonify({'vote': 'commit'})

@app.route('/commit', methods=['POST'])
def commit():
    data = request.json
    transaction_id = data['transaction_id']

    if transaction_id in transactions:
        transaction = transactions[transaction_id]
        if transaction['prepared']:
            if transaction['operation'] == 'addition':
                user_id = data['user_id']
                accounts[user_id]['lock'].acquire(blocking=True)
                accounts[user_id] += data['amount']
                accounts[user_id]['lock'].release()
                transaction['decision_received'].set()
                return jsonify({'status': 'committed'})
    return jsonify({'status': 'failed'}), 500

def timeout_check():
    while True:
        for transaction_id, transaction_state in list(transactions.items()):
            # Esperar por um tempo razoável (ex: 10 segundos)
            if not transaction_state.decision_received.wait(timeout=10):
                # Se o timeout foi atingido sem receber decisão, assumir aborto
                if transaction_state.prepared:
                    logging.warning(f'Timeout reached, aborting transaction: {transaction_state.transaction_data}')
                    transaction_state.prepared = False
                    transaction_state.transaction_data = None
                    transaction_state.lock.release()
                    del transactions[transaction_id]

@app.route('/transfer_op', methods=['POST'])
def start_transfer():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.json
    prepare_votes = []

    transaction_id = str(uuid.uuid4())

    # Fase 1: Preparação
    for msg in data:
        target_host, target_port = get_host(msg['bank'])
        msg['transaction_id'] = transaction_id
        try:
            response = requests.post(f'http://{target_host}:{target_port}/prepare', json=msg, timeout=5)
            prepare_votes.append(response.json()['vote'])
        except requests.exceptions.RequestException:
            prepare_votes.append('abort')
    
    # Decisão do Coordenador
    if all(vote == 'commit' for vote in prepare_votes):
        decision = 'commit'
    else:
        decision = 'abort'

    # Fase 2: Commit ou Abort
    for msg in data:
        target_host, target_port = get_host(msg['bank'])
        try:
            requests.post(f'{target_host}/{target_port}', json=msg)
        except requests.exceptions.RequestException:
            pass

    return jsonify({'decision': decision})