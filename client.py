# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 6789

# connect to the server on local computer
s.connect(('127.0.0.1', port))
s.send(str(5).encode())

# receive data from the server
print s.recv(1024)
print str(s.recv(1024).decode())
# close the connection
s.close()