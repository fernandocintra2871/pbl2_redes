from flask import Flask, request, jsonify
import logging
import threading

app = Flask(__name__)
logging.basicConfig(filename='participant.log', level=logging.INFO)

# Dicionário para armazenar o estado de cada transação
transactions = {}

class TransactionState:
    def __init__(self):
        self.prepared = False
        self.transaction_data = None
        self.lock = threading.Lock()
        self.decision_received = threading.Event()

@app.route('/prepare', methods=['POST'])
def prepare():
    data = request.json
    transaction_id = data['transaction_id']
    
    if transaction_id not in transactions:
        transactions[transaction_id] = TransactionState()
    
    transaction_state = transactions[transaction_id]
    
    # Reset the decision received event
    transaction_state.decision_received.clear()

    # Acquire lock
    locked = transaction_state.lock.acquire(blocking=False)
    if not locked:
        return jsonify({'vote': 'abort'})

    # Verificar se a operação pode ser preparada
    if data['amount'] > 0:  # Implementar lógica de verificação real aqui
        transaction_state.prepared = True
        transaction_state.transaction_data = data
        logging.info(f'Prepared transaction: {transaction_state.transaction_data}')
        return jsonify({'vote': 'commit'})
    else:
        transaction_state.lock.release()
        transaction_state.prepared = False
        return jsonify({'vote': 'abort'})

@app.route('/commit', methods=['POST'])
def commit():
    data = request.json
    transaction_id = data['transaction_id']
    
    if transaction_id in transactions:
        transaction_state = transactions[transaction_id]
        
        if transaction_state.prepared:
            # Executar a transação: debitar ou creditar conforme necessário
            if transaction_state.transaction_data:
                logging.info(f'Committing transaction: {transaction_state.transaction_data}')
                transaction_state.prepared = False
                transaction_state.transaction_data = None
                transaction_state.lock.release()
                transaction_state.decision_received.set()
                del transactions[transaction_id]
                return jsonify({'status': 'committed'})
    return jsonify({'status': 'failed'}), 500

@app.route('/abort', methods=['POST'])
def abort():
    data = request.json
    transaction_id = data['transaction_id']
    
    if transaction_id in transactions:
        transaction_state = transactions[transaction_id]
        
        # Desfazer a preparação
        if transaction_state.prepared:
            logging.info(f'Aborting transaction: {transaction_state.transaction_data}')
            transaction_state.prepared = False
            transaction_state.transaction_data = None
            transaction_state.lock.release()
            transaction_state.decision_received.set()
            del transactions[transaction_id]
            return jsonify({'status': 'aborted'})
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

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    # Iniciar thread de verificação de timeout
    threading.Thread(target=timeout_check, daemon=True).start()
    app.run(port=port)
