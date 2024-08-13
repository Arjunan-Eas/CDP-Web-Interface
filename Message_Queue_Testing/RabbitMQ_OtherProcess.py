import pika, sys, os, time

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'CDP_Queue'
x = 0

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    

    def callback(ch, method, properties, body):
        global x
        x += 1
        new_message = f'SDUID:TEST0001\nTOPIC:Status\nDATA:The rabbit has hopped {x} times!'
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=new_message)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    
    channel.start_consuming()

    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)