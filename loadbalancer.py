# first of all import the socket library
import errno
import socket
import time
import csv

import xlrd as xlrd
import xlwt
from xlwt import Workbook
from xlutils.copy import copy


server_cluster = {
    'c1': ['s1', 's2', 's3'],
    'c2': ['s4', 's5', 's6'],
    'c3': ['s7', 's8', 's9']
}

server_ip = {
    's1': '23.96.59.7', #Server1Machine
    's2': '40.71.85.31', #S1M1
    's3': '104.211.136.27', #S1M5
    's4': '40.117.154.129', #S2M1
    's5': '65.52.56.63', #S2M2
    's6': '168.62.107.91', #S2M3
    's7': '104.211.153.206', #S3M1
    's8': '104.211.154.136', #S3M2
    's9': '191.232.232.26' #S3M3
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

#Skeleton of the report
wb = Workbook()
# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')
sheet1.write(0, 0, 'Server No')
sheet1.write(1, 0, 'Server1')
sheet1.write(2, 0, 'Server2')
sheet1.write(3, 0, 'Server3')
sheet1.write(4, 0, 'Server4')
sheet1.write(5, 0, 'Server5')
sheet1.write(6, 0, 'Server6')
sheet1.write(7, 0, 'Server7')
sheet1.write(8, 0, 'Server8')
sheet1.write(9, 0, 'Server9')
wb.save('server_farming_result.xls',)


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
    # if ipquads[0] == '104' and ipquads[1] == '0':
    if ipquads[0] == '104':
        cluster = 'c1'
    elif ipquads[0] == '23':
        cluster = 'c2'
    elif ipquads[0] == '40' or ipquads[0] == '129':
        cluster = 'c3'
    return cluster

def main():
    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 6789

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        client_timeout = int(c.recv(5).decode())
        # send a thank you message to the client.
        response_to_client = '\nThank you for connecting to load balancer\n'
        c.send(response_to_client.encode())

        s2 = socket.socket()

        final_server = ''

        # Round robin phase when server is contacted less than 10 times
        global req_num
        rr_server = 's' + str(req_num % 9 + 1)
        if rr_server in list(server_req_count.keys()) and server_req_count[rr_server] < 10:
            final_server = rr_server
            server_req_count[rr_server] += 1

        req_num += 1

        # 2nd Phase of algorithm
        if not final_server:
            available_servers = []
            # Extracting class of servers based on client IP
            cluster_id = getserverlistbasedonclient(addr)
            server_list = server_cluster[cluster_id]

            # Iterate class of servers and determine available servers based on its availability and response time
            for server in server_list:
                if server_availability[server] and client_timeout > server_resp_times[server]:
                    available_servers.append(server)

            # Pick the server with highest efficiency
            max_efficiency = -1
            for server in available_servers:
                if server_resp_times[server] > 0 and server_busy_times[server][1] / server_resp_times[server] > max_efficiency:
                    max_efficiency = server_busy_times[server][1] / server_resp_times[server]
                    final_server = server

            if final_server == '':
                c.send('\nAll servers are currently busy, please try again later\n')
        if final_server:
            # Get port for this server
            port2 = server_ports[final_server]

            # connect to the server on local computer
            s2.connect((server_ip[final_server], port2))

            # start timer to calculate response time
            st = time.time()

            flags = str(s2.recv(14).decode())
            print(flags)

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
                # size = s2.recv(64)  # assuming that the size won't be bigger then 1GB
                # print size
                buffer = b""
                server_availability[final_server] = True
                print('Test 1')
                savefilename = 'filefromlb.mp4'
                s2.setblocking(0)
                with open(savefilename, 'wb') as file:
                    while True:
                        time.sleep(5)
                        try:
                            print('Test 2')
                            recvfile = s2.recv(4096)
                            print(recvfile)
                            buffer += recvfile
                            if not recvfile: break
                            file.write(recvfile)
                            print('Test 3')
                            # time.sleep(5)
                        except socket.error as e:
                            if e.args[0] == errno.EWOULDBLOCK:
                                print("Haay error aa gaya")
                                break
                print('Test 4')
                # with open(savefilename, 'rb') as file:
                #     sendfile = file.read()
                # if sendfile:
                #     c.sendall(sendfile)
                c.sendall(buffer)

                # if size.isdigit():
                #     size = int(size)
                #     current_size = 0
                #     while current_size < size:
                #         data = s2.recv(1024)
                #         if not data:
                #             break
                #         if len(data) + current_size > size:
                #             data = data[:size - current_size]  # trim additional data
                #         buffer += data
                #         # you can stream here to disk
                #         current_size += len(data)
                # else:
                #     buffer = size
                # # receive data from the server
                # c.send(buffer.encode())
                # Calculate response time
                resp_time = time.time() - st
                if server_resp_times[final_server] > 0:
                    server_resp_times[final_server] = (3 * server_resp_times[final_server] + resp_time) / 4
                else:
                    server_resp_times[final_server] = resp_time
                server_load[final_server] = int(flags.split(',')[0].split(':')[1])




        # with open('ServerResponseTimes', 'a') as respfile:
        #     respobj = csv.writer(respfile, delimiter=':')
        for resptime in list(server_resp_times.keys()):
            # print(resptime)
            if resptime==final_server:
                row_number = final_server.split("s")
                wb1 = xlrd.open_workbook('server_farming_result.xls')
                sheet2 = wb1.sheet_by_index(0)
                k = sheet2.row_values(int(row_number[1]))
                numCols=len(sheet2.row_values(int(row_number[1])))
                wb2 = copy(wb1)
                sheet3 = wb2.get_sheet(0)
                sheet3.write(0, int(numCols) - k.count(''),str(int(numCols) - k.count('')) )
                sheet3.write(int(row_number[1]),int(numCols)-k.count(''),server_resp_times[resptime])
                wb2.save('server_farming_result.xls')
            else:
                continue

        # print server_resp_times
        print(server_busy_times)
        print(server_load)

        # Close the connection with the client
        c.close()

if __name__ == '__main__':
    main()
