from flask import render_template
from flask_socketio import emit
from blockchain.core.blockchain import Blockchain
from blockchain.core.block import Block
from datetime import datetime
from api.server import create_app  # Correct import statement

# Initialize the Flask app and Socket.IO
app, socketio = create_app()

# Initialize the blockchain
julinks = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('blockchain_update', {'blocks': [block.__dict__ for block in julinks.chain]})

@socketio.on('mine_block')
def handle_mine_block():
    julinks.mine_pending_transactions()
    emit('blockchain_update', {'blocks': [block.__dict__ for block in julinks.chain]}, broadcast=True)

def main():
    # Run the Flask app with Socket.IO
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()