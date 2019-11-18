# Import socket module
import socket

# Create a socket object
def client_process():
    s = socket.socket()

    # Define the port on which you want to connect
    lb_port = 6789

    # connect to the server on local computer
    s.connect(('127.0.0.1', lb_port))

    # receive data from the server
    print (s.recv(1024))
    print (s.recv(1024))
    # close the connection
    s.close()

client_process()
client_process()
client_process()
client_process()