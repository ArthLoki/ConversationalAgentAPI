import pika

def openConnection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=500))
    return connection

def getChannel(connection):
    channel = connection.channel()
    return channel

def closeConnection(connection):
    connection.close()
    return
