from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_socketio import SocketIO
from datetime import datetime
import threading
import pika

# RabbitMQ configuration
RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'CDP_Queue'

# Instantiate a flask app and socketio object
app = Flask(__name__, static_url_path='/static')
socket = SocketIO(app)

# Function to establish RabbitMQ connection and declare queue
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    return connection, channel

# Function to consume messages from RabbitMQ
def consume_messages(socket):
    connection, channel = setup_rabbitmq()

    def callback(ch, method, properties, body):
        received_message = body.decode()
        socket.send(received_message)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# Main route for sending html page to client
@app.route('/')
def index():
    with open('CDP-Web-Interface\index.html', 'r') as f:
        return render_template_string(f.read())

# POST method that deals with message sent by client
@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = request.form['DUCK_TYPE']

    message = f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDUCK_TYPE:{text4}'
    
    connection, channel = setup_rabbitmq()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    connection.close()

    return redirect(url_for('index'))

socket.on("message")
def confirm_receipt(message):
    if(message == "Message received"):
        print("Message was successfully sent to client")

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consume_messages, args=(socket,))
    consumer_thread.daemon = True
    consumer_thread.start()
    socket.run(app, allow_unsafe_werkzeug=True)