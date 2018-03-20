import socket #Imported sockets module
import sys

HOST = 'localhost'
PORT = 12345
BUFSIZ = 256


# looks like "server001" and "client001" are done for python2 ONLY
if(sys.argv[1] == "client"):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input("Enter hostname [%s]: " %HOST) or HOST
    port = input("Enter port [%s]: " %PORT) or PORT
    sock_addr = (host, int(port))
    client_sock.connect(sock_addr)
    payload = 'GET TIME'
    try:
        while True:
            client_sock.send(payload.encode('utf-8'))
            data = client_sock.recv(BUFSIZ)
            print(repr(data))
            more = input("Want to send more data to server[y/n] :")
        if more.lower() == 'y':
            payload = input("Enter payload: ")
        else:
            pass
    except KeyboardInterrupt:
        print("Exited by user")
    client_sock.close()



elif(sys.argv[1] == "server"):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(HOST)
    server_socket.listen(5)
    server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    while True:
        print('Server waiting for connection...')
        client_sock, addr = server_socket.accept()
        print('Client connected from: ', addr)
        while True:
            data = client_sock.recv(BUFSIZ)
            if not data or data.decode('utf-8') == 'END':
                break
            print("Received from client: %s" % data.decode('utf-8'))
            print("Sending the server time to client: %s"%ctime())
            try:
                client_sock.send(bytes(ctime(), 'utf-8'))
            except KeyboardInterrupt:
                print("Exited by user")
                client_sock.close()
    server_socket.close()