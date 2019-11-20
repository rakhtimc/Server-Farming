# first of all import the socket library
import socket
import time
import threading
from Queue import Queue

# next create a socket object
from server import ProcessRequest

numthreads = 2
numjobs = 10
thread_queue = Queue()
s = socket
conns = []

def create_socket():
    global s
    s = s.socket()
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
    return s

def listen_conn(sock):
    st = time.time()
    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        sock.listen(50)
        print "socket is listening"
        # Establish connection with client.
        c, addr = sock.accept()

        print 'Got connection from', addr

        resp = ProcessRequest('')
        c.send(resp.handleRequest())

        # if len(conns) > 0 and (time.time() - st) > 2:
        #     conns.pop()
        #     st = time.time()

        conns.append(c)
        if len(conns) > numjobs:
            print 'Show Some Mercy on Server!!'
            c.send('Show Some Mercy on Server!!, number of conns: ' + str(len(conns)))
            c.close()
        else:
            print 'Got connection from', addr

            resp = ProcessRequest('')
            c.send(resp.handleRequest() + ', number of conns: ' + str(len(conns)))

            if len(conns) > 0 and (time.time() - st) > 0.1:
                conns.pop()
                st = time.time()

def thread_work():
    for _ in range(numthreads):
        global s
        while True:
            x = thread_queue.get()
            # listen_conn(s)
            if x == 1:
                s = create_socket()
                listen_conn(s)
            elif x == 2:
                listen_conn(s)

            thread_queue.task_done()

def create_workers():
    t = threading.Thread(target=thread_work)
    t.daemon = True
    t.start()

def create_jobs():
    i = 0
    while i < numthreads:
        thread_queue.put(i)
        i = i + 1
    thread_queue.join()

def main():
    # global s
    # s = create_socket()
    # listen_conn(s)
    create_workers()
    create_jobs()

if __name__ == '__main__':
    main()