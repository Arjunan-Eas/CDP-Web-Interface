import redis
from flask import Flask, render_template, request, redirect, url_for, render_template_string
from flask_socketio import SocketIO

# Redis streams configuration
REDIS_HOST = "localhost"
STREAM_NAME = "mystream"
CONSUMER_GROUP = "webGroup"
CONSUMER_NAME = "webConsumer"
INBOUND_KEY = "CDP_WEB"
OUTBOUND_KEY = "WEB_CDP"

# Instantiate a Flask app and SocketIO object
app = Flask(__name__, static_url_path='/static')
socket = SocketIO(app)

# Connect to redis server and create consumer group
redis_stream = redis.Redis(host=REDIS_HOST, port=6379)

def redis_init():
    # Create consumer group for web portal
    try:
        redis_stream.xgroup_create(STREAM_NAME, CONSUMER_GROUP, id=0, mkstream=True)
    # Handle exception raised when group already exists
    except(redis.exceptions.ResponseError):
        print("group already created")
    
    # Check for left over pending messages
    pend_reply = redis_stream.xpending(STREAM_NAME, CONSUMER_GROUP)
    print(pend_reply)

    if(pend_reply == None):
        print("Pending message check error")
    # Acknowledge any left over pending messages
    elif(pend_reply['pending'] > 0):
        detailed_reply = redis_stream.xpending_range(STREAM_NAME, CONSUMER_GROUP, pend_reply['min'], pend_reply['max'], pend_reply['pending'])
        for message in detailed_reply:
            redis_stream.xack(STREAM_NAME, CONSUMER_GROUP, message['message_id'])

def parse_reply(reply):
    # Iterate through all messages read from xread_group
    for message in reply[0][1]:
        # Only will attempt to parse inbound messages
        if list(message[1].keys())[0] == INBOUND_KEY.encode():
            # Slice string to get components
            message_content = message[1][INBOUND_KEY.encode()]
            content_list = message_content.decode().split('\0')[:-1]
            sduid = content_list[0][len("SDUID:") : ]
            topic = content_list[1][len("TOPIC:") : ]
            data = content_list[2][len("DATA:") : ]
            # Send message out to client side
            message_to_client(sduid, topic, data)
            
        # Ack message regardless of inbound/outbound
        redis_stream.xack(STREAM_NAME, CONSUMER_GROUP, message[0])

def message_to_client(SDUID, topic, data):
    # Format information how client expects to receive it
    formatted_string = f'SDUID:{SDUID}\nTOPIC:{topic}\nDATA:{data}'
    socket.send(formatted_string)

def check_messages():
    reply = redis_stream.xreadgroup(CONSUMER_GROUP, CONSUMER_NAME, {STREAM_NAME:'>'})
    if(len(reply)):
        parse_reply(reply)

# Main route for sending HTML page to the client
@app.route('/')
def index():
    with open('CDP-Web-Interface/index.html', 'r') as f:
        return render_template_string(f.read())

# POST method that deals with message sent by client
@app.route('/submit', methods=['POST'])
def submit():
    text1 = request.form['DUID']
    text2 = request.form['TOPIC']
    text3 = request.form['DATA']
    text4 = request.form['DUCK_TYPE']

    # Add the message to the Redis stream
    redis_stream.xadd(STREAM_NAME, {OUTBOUND_KEY:f'DUID:{text1}\0TOPIC:{text2}\0DATA:{text3}\0DUCK_TYPE:{text4}\0'})

    # Check for any new messages
    check_messages()

    return redirect(url_for('index'))

# Checks for message upon client side polling message
@socket.on('message')
def poll(message):
    if message == "polling":
        check_messages()

if __name__ == '__main__':
    redis_init()    # Initialize redis
    socket.run(app, allow_unsafe_werkzeug=True)