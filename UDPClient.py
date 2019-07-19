from socket import *
serverAddress = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)


data = input('Input lowercase sentence: ')
dataBytes =  data.encode()
clientSocket.sendto(dataBytes, serverAddress)
modifiedData, serverAddress = clientSocket.recvfrom(2048)
print('From Server: ', modifiedData)
clientSocket.close()
