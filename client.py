# Import socket module
import socket

# connect to the server on local computer
def main():
    # Create a socket object
    s = socket.socket()
    # Define the port on which you want to connect
    port = 6789
    s.connect(('23.96.58.37', port))
    s.send(str(5).encode())

    # receive data from the server
    print(s.recv(1024).decode())
    savefilename = 'fileatclient.divx'
    with open(savefilename,'wb') as file:
        while True:
            recvfile = s.recv(4096)
            if not recvfile: break
            file.write(recvfile)
    # close the connection
    s.close()

if __name__ == '__main__':
    main()