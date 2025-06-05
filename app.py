import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Arduino Dashboard Online"

@app.route('/api/data', methods=['POST'])
def receive_data():
    content = request.json
    print(f"Received from forwarder: {content}")
    socketio.emit('serial_data', content)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
