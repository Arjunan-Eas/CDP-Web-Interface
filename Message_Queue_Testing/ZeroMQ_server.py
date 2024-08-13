from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_socketio import SocketIO
from datetime import datetime
import threading
import zmq

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'CDP_Queue'

# Instantiate a flask app and socketio object
app = Flask(__name__, static_url_path='/static')
flask_socket = SocketIO(app)


# Function to establish zmq connection
context = zmq.Context()
zmq_socket = context.socket(zmq.PAIR)
zmq_socket.bind("tcp://*:5555")

# Function to consume messages from client side
def consume_messages(flask_socket, zmq_socket):
    while True:
        message = zmq_socket.recv()
        print(f"Message: {message}")
        flask_socket.send(message.decode())
        

# Main route for sending html page to client
@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return render_template_string(f.read())

# POST method that deals with message sent by client
@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    text6 = 0

    message = f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}\nREAD_STATE:{text6}'

    zmq_socket.send_string(message)

    return redirect(url_for('index'))

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume_messages, args=(flask_socket,zmq_socket,))
    consumer_thread.daemon = True
    consumer_thread.start()
    flask_socket.run(app, allow_unsafe_werkzeug=True)