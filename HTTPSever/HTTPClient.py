from socket import *
# Server address is the network, external IP
# Router must be configured to forward port traffic to local ip and port
serverAddress = ('217.138.134.182', 3080)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)
print("\nConnected to server...")

HTTPRequest = open("HTTPRequest.txt", "r")
HTTPMessage = HTTPRequest.read()
messageBytes =  HTTPMessage.encode()
clientSocket.send(messageBytes)
print("\nMessage sent.")

while True:
    serverData = clientSocket.recv(1024)
    if len(serverData) > 0:
        print('From Server:\n\n', serverData.decode('utf-8')[:])
# clientSocket.close()
