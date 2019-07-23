from socket import *
serverAddress = ('localhost', 12000)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

print("The Server is ready to receive...")
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.upper()
    serverSocket.sendto(modifiedMessage, clientAddress)
