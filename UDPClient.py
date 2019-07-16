from socket import *
serverAddress = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence: ')
messageBytes =  message.encode()
clientSocket.sendto(messageBytes, serverAddress)
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()
