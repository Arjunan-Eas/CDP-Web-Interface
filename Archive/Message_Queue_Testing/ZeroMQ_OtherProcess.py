import zmq, os, sys



def main():
    context = zmq.Context()
    print("Connecting to hello world server…")
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://localhost:5555")

    while True:
        message = socket.recv()

        message_DUID = "Received DUID: " + message.decode()[5:13]
        print(message_DUID)
        socket.send_string(f'DUID:a_duid__\nTOPIC:q=a_topic\nDATA:Your message was received\nDATE:now\nTIME:00:00\nREAD_STATE:0')

main()