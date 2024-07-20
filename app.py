"""
Code is provided to run the server locally on your computer for testing, or on the Pi. 
Comment out the unused line to switch between modes.

"""


# Flask is the service used to build the server
from flask import Flask, render_template, request, redirect, url_for, render_template_string

# Socketio is used to establish unidirectional communication between the client and server
from flask_socketio import SocketIO

from datetime import datetime

# Threading allows parallel processes to take place
import threading

# Watchdog is a file monitoring service
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Instantiate a flask app and socketio object
app = Flask(__name__)
socket = SocketIO(app)

# Custom class to monitor file changes
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, socket, filename):
        self.socket = socket
        self.filename = filename

    def on_modified(self, event):
        # if event.src_path.endswith(self.filename[-21:-1]):
        if event.src_path.endswith(self.filename[2:]):
            with open(self.filename, 'r') as f:     # Send the contents of the received message to the client
                received_message = list(f.read())
                received_message = "".join([char for char in received_message if char != '\n'])
                self.socket.send(received_message)

# Initialization function for watchdog
def start_watching(socket, filename):
    event_handler = FileChangeHandler(socket, filename)
    observer = Observer()
    # observer.schedule(event_handler, path='/home/ubuntu/webapp/messaging/', recursive=False)
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Main route for sending html page to client
@app.route('/')
def index():
    # return render_template('index.html')
    with open('new_index.html', 'r') as f:
        return render_template_string(f.read())

# POST method that deals with message sent by client
@app.route('/submit', methods=['POST'])
def submit():
    # Get the contents of the form on the webpage
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    text6 = 0
    # with open('/home/ubuntu/webapp/messaging/received_message.txt', 'w') as f:
    # with open('received_message.txt', 'w') as f:
        # f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:Your message was: {text3}\nDATE:{text4}\nTIME:{text5}\nREAD_STATE:{text6}')
    # with open('/home/ubuntu/webapp/messaging/sent_message.txt', 'w') as f:
    with open('sent_message.txt', 'w') as f:
        f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}\nREAD_STATE:{text6}')
    return redirect(url_for('index'))

# Event when a message is received via socket
socket.on("message")
def modify_read_state(message):
    if message == "Message received":   # Checks if message is confirmation of receipt
        # with open('/home/ubuntu/webapp/messaging/received_message.txt', 'r+b') as f:
        with open('received_message.txt', 'r+b') as f:
            f.seek(0, 2)
            if f.tell() > 0:
                f.seek(-1, 2)
                f.write(b"1")   # Changes read state of received message

if __name__ == '__main__':
    # filename = '/home/ubuntu/webapp/messaging/received_message.txt'
    filename = 'received_message.txt'
    watcher_thread = threading.Thread(target=start_watching, args=(socket, filename))
    watcher_thread.daemon = True
    watcher_thread.start()
    # socket.run(app, host='10.42.0.1', allow_unsafe_werkzeug=True)
    socket.run(app, allow_unsafe_werkzeug=True)