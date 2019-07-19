from socket import *
serverAddress = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddress)

data = input('Input lowercase sentence: ')
dataBytes =  data.encode()
clientSocket.send(dataBytes)
modifiedData = clientSocket.recv(1024)
print('From Server: ' , modifiedData)
clientSocket.close()
