# first of all import the socket library
import socket

def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res

# next create a socket object
s = socket.socket()
print "Socket successfully created"

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 6789

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print "socket binded to %s" % (port)

# put the socket into listening mode
s.listen(5)
print "socket is listening"

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print 'Got connection from', addr

    # send a thank you message to the client.
    c.send('Thank you for connecting to load balancer')

    s2 = socket.socket()
    port2 = 12345

    # connect to the server on local computer
    s2.connect(('127.0.0.1', port2))

    size = s2.recv(16)  # assuming that the size won't be bigger then 1GB
    print size
    size = int(size)
    current_size = 0
    buffer = b""
    while current_size < size:
        data = s2.recv(1024)
        if not data:
            break
        if len(data) + current_size > size:
            data = data[:size - current_size]  # trim additional data
        buffer += data
        # you can stream here to disk
        current_size += len(data)

    # receive data from the server
    c.send(buffer.encode())
    # close the connection
    #s.close()

    # Close the connection with the client
    c.close()