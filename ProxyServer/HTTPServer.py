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
### Functionality limited to HTTP GET requests


class ProxyServer:
    """Proxy Server class"""
    def __init__(self, address='localhost', port=4001, ):
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
        print(f'Web server listening on {self.port}. Ready to serve...')
        # wait for client connection
        while True:
            self.manage_connections()
        # close connection
        self.socket.close()

    def manage_connections(self):
        """Process incoming connections via threading"""
        # establish the connection
        tcpCliSock, CliAddr = self.socket.accept()
        print('Received a connection from: ', CliAddr)
        # create thread to process request
        process = threading.Thread(name=CliAddr, \
                                   target = self.request_handle, \
                                   args=(tcpCliSock, CliAddr))
        # set thread process to daemon (terminate when sock closes)
        process.setDaemon(True)
        # start threaded processing of request
        process.start()

    def request_handle(self, tcpCliSock, CliAddr):
        try:
            # receive message from client
            message = tcpCliSock.recv(1024)
            messageStr = message.decode("utf-8")
            print(f"Message received from: {CliAddr}\n", \
                  messageStr.split()[0], ' ', messageStr.split()[1])
            # identify file requested (assumes message is get request)
            filename = messageStr.split()[1]
            # prepare file to Send
            f = open(filename[1:])
            data = f.read()
            dataBytes = data.encode()
            # send HTTP header
            tcpCliSock.send('\nHTTP/1.1 200 OK\n\n'.encode())
            # send file to client
            tcpCliSock.send(dataBytes)
            print(f"Data sent to {CliAddr}.")
        except IOError:
            # response header for file not found
            connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
            connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
        # close connection with client
        tcpCliSock.close()
        print(f"Connect on closed with client {CliAddr}.")


########################################################################
########################################################################

def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":

    print(f"Initiation timestamp: {get_timestamp()}")

    proxyServer = ProxyServer()

    print(f"Completion timestamp: {get_timestamp()}")

    print("Done!")
