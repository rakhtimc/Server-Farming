# first of all import the socket library
import socket
import time

server_cluster = {
    'c1': ['s1', 's2', 's3'],
    'c2': ['s4', 's5', 's6'],
    'c3': ['s7', 's8', 's9']
}

server_ip = {
    's1': '127.0.0.1',
    's2': '127.0.0.1',
    's3': '127.0.0.1',
    's4': '127.0.0.1',
    's5': '127.0.0.1',
    's6': '127.0.0.1',
    's7': '127.0.0.1',
    's8': '127.0.0.1',
    's9': '127.0.0.1'
}

server_load = {
    's1': 0,
    's2': 0,
    's3': 0,
    's4': 0,
    's5': 0,
    's6': 0,
    's7': 0,
    's8': 0,
    's9': 0
}

server_busy_times = {
    's1': [0, 0],
    's2': [0, 0],
    's3': [0, 0],
    's4': [0, 0],
    's5': [0, 0],
    's6': [0, 0],
    's7': [0, 0],
    's8': [0, 0],
    's9': [0, 0]
}

server_resp_times = {
    's1': 0,
    's2': 0,
    's3': 0,
    's4': 0,
    's5': 0,
    's6': 0,
    's7': 0,
    's8': 0,
    's9': 0
}

server_availability = {
    's1': True,
    's2': True,
    's3': True,
    's4': True,
    's5': True,
    's6': True,
    's7': True,
    's8': True,
    's9': True
}

server_ports = {
    's1': 12345,
    's2': 12346,
    's3': 12347,
    's4': 12348,
    's5': 12349,
    's6': 12350,
    's7': 12351,
    's8': 12352,
    's9': 12353
}

server_req_count = {
    's1': 0,
    's2': 0,
    's3': 0,
    's4': 0,
    's5': 0,
    's6': 0,
    's7': 0,
    's8': 0,
    's9': 0
}

req_num = 0

ports = []


def bytes_to_number(b):
    # if Python2.x
    # b = map(ord, b)
    res = 0
    for i in range(4):
        res += b[i] << (i * 8)
    return res


def getserverlistbasedonclient(addr):
    cluster = ''
    ipquads = str(addr[0]).split('.')
    if ipquads[0] == '127' and ipquads[1] == '0':
        if ipquads[2] == '0':
            cluster = 'c1'
        elif ipquads[2] == '1':
            cluster = 'c2'
        elif ipquads[2] == '2':
            cluster = 'c3'
    return cluster


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

    client_timeout = int(c.recv(5).decode())
    # send a thank you message to the client.
    c.send('\nThank you for connecting to load balancer\n')

    s2 = socket.socket()

    final_server = ''

    # Round robin phase when server is contacted less than 10 times
    rr_server = 's' + str(req_num % 9 + 1)
    if rr_server in server_req_count.keys() and server_req_count[rr_server] < 10:
        final_server = rr_server
        server_req_count[rr_server] += 1

    req_num += 1

    # 2nd Phase of algorithm
    if not final_server:
        available_servers = []
        # TODO Extracting class of servers based on client IP
        cluster_id = getserverlistbasedonclient(addr)
        server_list = server_cluster[cluster_id]

        # TODO Iterate class of servers and determine available servers based on its availability and response time
        for server in server_list:
            if server_availability[server] and client_timeout > server_resp_times[server]:
                available_servers.append(server)

        # TODO Pick the server with highest efficiency
        max_efficiency = -1
        for server in available_servers:
            if server_resp_times[server] > 0 and server_busy_times[server][1] / server_resp_times[server] > max_efficiency:
                max_efficiency = server_busy_times[server][1] / server_resp_times[server]
                final_server = server

        if final_server == '':
            c.send('\nAll servers are currently busy, please try again later\n')
    if final_server:
        # TODO Get port for this server
        port2 = server_ports[final_server]

        # connect to the server on local computer
        s2.connect((server_ip[final_server], port2))

        # start timer to calculate response time
        st = time.time()

        flags = str(s2.recv(14).decode())
        print flags

        if flags.find('SB') != -1:
            ct = time.time()
            if server_busy_times[final_server][1] > 0:
                pt = server_busy_times[final_server][0]
                server_busy_times[final_server].append(ct)
                server_busy_times[final_server].append(3 * server_busy_times[final_server][1] + (ct - pt) / 4)
            else:
                server_busy_times[final_server].append(ct)
                server_busy_times[final_server].append(ct)
            server_busy_times[final_server].pop(0)
            server_busy_times[final_server].pop(1)
            server_availability[final_server] = False
            c.send('\nServer is Busy, Please try after sometime\n')
        else:
            size = s2.recv(64)  # assuming that the size won't be bigger then 1GB
            print size
            buffer = b""
            server_availability[final_server] = True
            if size.isdigit():
                size = int(size)
                current_size = 0
                while current_size < size:
                    data = s2.recv(1024)
                    if not data:
                        break
                    if len(data) + current_size > size:
                        data = data[:size - current_size]  # trim additional data
                    buffer += data
                    # you can stream here to disk
                    current_size += len(data)
            else:
                buffer = size
            # receive data from the server
            c.send(buffer.encode())
            # Calculate response time
            resp_time = time.time() - st
            if server_resp_times[final_server] > 0:
                server_resp_times[final_server] = (3 * server_resp_times[final_server] + resp_time) / 4
            else:
                server_resp_times[final_server] = resp_time
            server_load[final_server] = int(flags.split(',')[0].split(':')[1])
    print server_resp_times
    print server_busy_times
    print server_load

    # Close the connection with the client
    c.close()
