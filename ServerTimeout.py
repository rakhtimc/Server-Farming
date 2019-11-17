# first of all import the socket library
import socket
import time

# next create a socket object
from server import ProcessRequest




s = socket.socket()
print "Socket successfully created"

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

request_count = 0
conns = []

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print "socket binded to %s" % (port)
st = time.time()
# a forever loop until we interrupt it or
# an error occurs
while True:
    s.listen(10000)
    print "socket is listening"
    # Establish connection with client.
    c, addr = s.accept()

    conns.append(c)

    if len(conns) > 2:
        print 'Show Some Mercy on Server!!'
        c.send('Show Some Mercy on Server!!')
        c.close()
    else:
        print 'Got connection from', addr

        # send a thank you message to the client.
        resp = ProcessRequest('')
        c.send(resp.handleRequest())

        if len(conns) > 0 and (time.time() - st) > 2:
            conns.pop()
            st = time.time()
        # Close the connection with the client
        # time.sleep(request_count)
        # c.close()