# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('input', namespace='/terminal')
def handle_input(data):
    command = data['input']
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/bash', preexec_fn=lambda: os.setuid(0)
    )
    stdout, stderr = process.communicate()
    response = stdout.decode() + stderr.decode()
    emit('output', {'output': response})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
