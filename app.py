from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# === Serial Configuration ===
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600

def serial_listener():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
#               print(f"[Serial] {line}")
                socketio.emit('serial_data', {'line': line})
    except serial.SerialException as e:
        print(f"Serial error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Start serial listener thread
    threading.Thread(target=serial_listener, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
