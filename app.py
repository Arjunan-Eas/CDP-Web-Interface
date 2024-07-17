from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_socketio import SocketIO
from datetime import datetime
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
socket = SocketIO(app)

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, socket, filename):
        self.socket = socket
        self.filename = filename

    def on_modified(self, event):
        if event.src_path.endswith(self.filename[-21:-1]):
        # if event.src_path.endswith(self.filename[2:]):
            with open(self.filename, 'r') as f:
                received_message = list(f.read())
                received_message = "".join([char for char in received_message if char != '\n'])
                self.socket.send(received_message)

def start_watching(socket, filename):
    event_handler = FileChangeHandler(socket, filename)
    observer = Observer()
    observer.schedule(event_handler, path='/home/ubuntu/webapp/messaging/', recursive=False)
    # observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.route('/')
def index():
    return render_template('index.html')
    # with open('new_index.html', 'r') as f:
    #     return render_template_string(f.read())

@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = str(datetime.now())[:10]
    text5 = str(datetime.now())[11:19]
    text6 = 0
    # with open('/home/ubuntu/webapp/messaging/received_message.txt', 'w') as f:
    # with open('received_message.txt', 'w') as f:
        # f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:Your message was: {text3}\nDATE:{text4}\nTIME:{text5}\nREAD_STATE:{text6}')
    with open('/home/ubuntu/webapp/messaging/sent_message.txt', 'w') as f:
    # with open('sent_message.txt', 'w') as f:
        f.write(f'DUID:{text1}\nTOPIC:{text2}\nDATA:{text3}\nDATE:{text4}\nTIME:{text5}\nREAD_STATE:{text6}')
    return redirect(url_for('index'))

socket.on("message")
def modify_read_state(message):
    if message == "Message received":
        with open('/home/ubuntu/webapp/messaging/received_message.txt', 'r+b') as f:
        # with open('received_message.txt', 'r+b') as f:
            # Ensure the file is long enough
            f.seek(0, 2)  # Move to the end of the file
            if f.tell() > 0:
                f.seek(-1, 2)
                f.write(b"1")

if __name__ == '__main__':
    filename = '/home/ubuntu/webapp/messaging/received_message.txt'
    # filename = 'received_message.txt'
    watcher_thread = threading.Thread(target=start_watching, args=(socket, filename))
    watcher_thread.daemon = True
    watcher_thread.start()
    socket.run(app, host='10.42.0.1', allow_unsafe_werkzeug=True)
    # socket.run(app, allow_unsafe_werkzeug=True)