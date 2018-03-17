import socket #Imported sockets module
import sys




# looks like "server001" and "client001" are done for python2 ONLY
if(sys.argv[1] == "server"):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 8090 #Reserve a port
    BUFFER_SIZE = 1024
    try:
        #Create an AF_INET (IPv4), STREAM socket (TCP)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, e):
        print ('Error occurred while creating socket. Error code: ' + str(e[0]) + ' , Error message : ' + e[1])
        sys.exit();
    tcp_socket.bind((TCP_IP, TCP_PORT))
    # Listen for incoming connections (max queued connections: 2)
    tcp_socket.listen(2)
    print ('Listening..')
    #Waits for incoming connection (blocking call)
    connection, address = tcp_socket.accept()
    print ('Connected with:', address)
    print (connection.recv(BUFFER_SIZE))

elif(sys.argv[1] == "client"):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 8090 # Reserve a port
    BUFFER_SIZE = 1024
    MESSAGE_TO_SERVER = b"Hello, World!"    # here is the difference if this wass run with py2.7.. you just omit the b
    try:
        #Create an AF_INET (IPv4), STREAM socket (TCP)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, e):
        print ('Error occured while creating socket. Error code: ' + str(e[0]) + ' , Error message : ' + e[1])
        sys.exit();
    tcp_socket.connect((TCP_IP, TCP_PORT))
    try :
        #Sending message
        tcp_socket.send(MESSAGE_TO_SERVER)
    except socket.error as e:
        print ('Error occurred while sending data to server. Error code: ' + str(e[0]) + ' , Error message : ' + e[1] )
        sys.exit()
    print ('Message to the server send successfully')
    # data = tcp_socket.recv(BUFFER_SIZE)
    tcp_socket.close() #Close the socket when done
    # print ("Response from server:", data)