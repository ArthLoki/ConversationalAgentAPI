# def sendMessage(channel, connection, queue_name: str, message: str):
#     channel.queue_declare(queue=queue_name)
#     channel.basic_publish(exchange='', routing_key=queue_name, body=message)
#     print(f" [x] Sent {message}")


#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()