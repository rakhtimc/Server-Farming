# first of all import the socket library
import socket

# next create a socket object
def loadbal_process():
    s = socket.socket()
    print ("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 6789

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print ("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print ("socket is listening")

    sever_req_count = 0
    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        print ('new')
        c, addr = s.accept()
        print ('Got connection from', addr)

        # send a thank you message to the client.
        c.send('Thank you for connecting to load balancer')

        sever_req_count = sever_req_count + 1

        s2 = socket.socket()

        # if(sever_req_count%2 == 1):
        #     port2 = 12345
        # else:
        #     port2 = 45678

        if (addr[1]^11000 >=50000 and addr[1]^11000 <=60000):
            port2 = 12345
        else:
            port2 = 45678



        # connect to the server on local computer
        s2.connect(('127.0.0.1', port2))
        # receive data from the server
        c.send(s2.recv(1024))
        # close the connection
        # s.close()

        # Close the connection with the client
        c.close()

loadbal_process()