#!/usr/bin/env python

# standard Python libraries
import time
from socket import *

# third party Python libraries

# custom Python libraries

# testing notes

# config notes
### Server address is the network, external IP
### Router must be configured to forward port traffic to local ip and port


class ClientServer:
    def __init__(self):
        """Initial TCP Client Server (HTML)"""
        # create TCP server socket
        self.socket = socket(AF_INET, SOCK_STREAM)

    def connect(self, serverAddress, serverPort):
        """Connect to server"""
        self.socket.connect((serverAddress, serverPort))
        print(f"Connected to server: {serverAddress}:{serverPort}")
        print(f"Ready to send...")

    def send(self, message):
        """Send request message to server"""
        # encode message into bytes
        messageBytes =  message.encode()
        # send message to server
        self.socket.send(messageBytes)
        print("\nRequest message sent.")
        # wait for and handle response
        print(f"Data from Server:\n")
        while True:
            # accept data from server with byte limit
            try:
                serverData = self.socket.recv(1024)
                if len(serverData) > 0:
                    print(f"{serverData.decode('utf-8')}")
                else:
                    self.terminate()
                    break
            except:
                self.terminate()
                break

    def terminate(self):
        """Terminate connection and tear down socket"""
        self.socket.close()
        print('Socket closed.')




########################################################################
########################################################################

def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S")

if __name__ == "__main__":

    print(f"Initiation timestamp: {get_timestamp()}")

    CServer = ClientServer()
    address='localhost'
    port=4001
    CServer.connect(address, port)
    HTTPRequest = open("HTTPRequest.txt", "r")
    message = HTTPRequest.read()
    CServer.send(message)

    print(f"Completion timestamp: {get_timestamp()}")

    print("Done!")
