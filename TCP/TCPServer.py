import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 555

serversocket.bind((host, port))

serversocket.listen(2)

while True:
    
    clientsocket, address = serversocket.accept()

    print('Received connection')

    message = 'Hello World' + '\r\n'
    clientsocket.send(message.encode('ascii'))

    clientsocket.close()


