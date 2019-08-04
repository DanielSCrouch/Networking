#!/usr/bin/env python

# standard Python libraries
import time
from socket import *
import sys
import threading

# third party Python libraries

# custom Python libraries

# testing notes
file = open('TestFile.txt', 'rb').read()

# config notes
### Server address is the network, external IP
### Router must be configured to forward port traffic to local ip and port
### python3 ProxyServer.py http://localhost:8888/www.google.com


class ProxyServer:
    """Proxy Server class"""
    def __init__(self, address='localhost', port=4001):
        """Iniitialize ProxyServer class object"""
        # define public ip and port address
        # localhost for loopback to host machine
        self.address = 'localhost'
        self.port = port
        # create TCP server socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        # set socket to reusable
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # bind socket to the port
        self.socket.bind((self.address, self.port))
        # listen for inbound communication to port
        self.socket.listen(1)
        print(f'Web server listening on {self.port}. Ready to serve...\n')
        # wait for client connection
        while True:
            self.manage_connections()
        # close connection
        self.socket.close()

    def manage_connections(self):
        """Process incoming connections via threading"""
        # establish the connection
        tcpCliSock, CliAddr = self.socket.accept()
        print(f'Received a connection from: {CliAddr}\n')
        # create thread to process request
        process = threading.Thread(name=CliAddr, \
                                   target = self.request_handle, \
                                   args=(tcpCliSock, CliAddr))
        # set thread process to daemon (terminate when sock closes)
        process.setDaemon(True)
        # start threaded processing of request
        process.start()

    def request_handle(self, tcpCliSock, CliAddr):
        # receive message from client
        message = tcpCliSock.recv(1024)
        messageStr = message.decode("utf-8")
        print(f"Message: \n{messageStr.split()[0]} {messageStr.split()[1]}\n")
        # identify file requested (assumes message is get request)
        filename = messageStr.split()[1]
        print('filename: ', filename)
        try:
            # try to retrieve data from cache
            dataBytes = self.retrieve_from_cache(filename)
            # send HTTP header
            tcpCliSock.send('\nHTTP/1.1 200 OK\n\n'.encode())
            # send file to client
            tcpCliSock.send(dataBytes)
            print(f"Data sent from cache")
        except OSError as e:
            print(f"Cache error: {e}")
            try:
                # try to retrieve data from website
                dataBytes = self.retrieve_from_external(filename)
            except:
                # send response header for file not found
                connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
                connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())

        # close connection with client
        tcpCliSock.close()
        print(f"Connect on closed with client {CliAddr}.")

    def retrieve_from_cache(self, filename):
        try:
            # try to find file in cache
            f = open(f"./{filename}")
            data = f.read()
            dataBytes = data.encode()
            return dataBytes
        except Exception as e:
            raise OSError('File not found.')

    def retrieve_from_external(self, filename):
        try:
            # try to find file in cache
            f = open(f"./{filename[1:]}")
            data = f.read()
            dataBytes = data.encode()
            return dataBytes
        except Exception as e:
            raise OSError('File not found.')


#     message = serverSocket.recv(1024)
#     print('Message received: \n', message)
#     # Extract the filename from given message and print
#     filename = message.split()[1].partition("/")[2]
#     print('Filename: ', filename)
#     fileExist = "false"
#     filetouse = "/" + filename
#     print(filetouse)
#     try:
#     # Check wether the file exist in the cache
#         f = open(filetouse[1:], "r")
#         outputdata = f.readlines()
#         fileExist = "true"
#         # ProxyServer finds a cache hit and generates a response message
#         tcpCliSock.send("HTTP/1.0 200 OK\r\n")
#         # add headers optional
#         tcpCliSock.send("Content-Type:text/html\r\n")
#         tcpCliSock.send("\n\n" + outputdata) # Check functions as expected ???
#         print('Read from cache')
#     # Error handling for file not found in cache
#     except IOError:
#         if fileExist == "false":
#             hostAddress = ('localhost', 80)
#             clientSocket = socket(AF_INET, SOCK_STREAM)
#             hostn = filename.replace('www.','',1)
#             print('Host Name: ', hostn)
#             try:
#                 clientSocket.connect(hostAddress)
#                 # Create a temporary file on this sicket and ask port 80 for the file requested by the cient
#                 fileobj = clientSocket.makefile('r', 0)
#                 fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
#                 # Read the response into buffer
#                 clientSocket.send(fileobj)
#                 buffer = clientSocket.recv(2048)
#                 tcpCliSock.send(buffer)
#             except:
#                 print('Illegal request')
#
#         else:
#             # HTTP response message for file not found
#             continue
#     clientSocket.close()
# serverSocket.close()


########################################################################
########################################################################

def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":

    print(f"Initiation timestamp: {get_timestamp()}")

    proxyServer = ProxyServer()

    print(f"Completion timestamp: {get_timestamp()}")

    print("Done!")
