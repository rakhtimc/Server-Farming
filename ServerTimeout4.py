# first of all import the socket library
import os
import socket
import time
import threading
import sys
from queue import Queue

# next create a socket object
from server import ProcessRequest

numthreads = 2
numjobs = 10
thread_queue = Queue()
s = socket
conns = []
numconns = 0

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def create_socket():
    global s
    s = s.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12348 but it can be anything
    port = 12348

    request_count = 0
    conns = []

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print("socket binded to %s" % (port))
    return s

def listen_conn(sock):
    global numconns
    global conns
    st = time.time()
    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        sock.listen(50)
        print("socket is listening")

        if len(conns) > 0 and (time.time() - st) > 0.01:
            conns.pop()
            st = time.time()

        if (time.time() - st) > 2 and len(conns) == numconns:
            conns = []
        # Establish connection with client.
        c, addr = sock.accept()

        print('Got connection from', addr)

        conns.append(c)

        numconns = len(conns)
        strconns = str(numconns)
        if numconns < 10:
            strconns = '0' + strconns

        flags = 'NumConns:' + strconns
        if len(conns) > numjobs:
            flags += ',SB'
            print('Show Some Mercy on Server!!')
            print(flags)
            c.send(str(flags).encode())
            c.close()
        else:
            print('Got connection from', addr)
            flags += ',NB'

            resp = ProcessRequest('')
            filename = resp.handleRequest()
            c.send(str(flags).encode())

            if os.path.exists(filename):
                length = os.path.getsize(filename)
                print(length)
                # flags = '127.0.0.1,NumConns:' + str(len(conns))
                # c.send(str(length).encode())  # has to be 4 bytes
                with open(filename, 'rb') as file:
                    d = file.read()
                if d:
                    c.sendall(d)

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