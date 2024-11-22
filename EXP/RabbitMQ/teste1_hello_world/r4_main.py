from r1_connections import openConnection, getChannel, closeConnection
from r2_sendMessage import sendMessage
from r3_receiveMessage import receiveMessage


def main():
    connection = openConnection()
    channel = getChannel(connection)

    queue_name = input("Enter a queue name: ")
    message = input("Enter a message: ")

    connection = openConnection()
    channel = getChannel(connection)

    receiveMessage(channel, queue_name, message)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    sendMessage(channel, connection, queue_name, message)
    closeConnection(connection)
    return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
