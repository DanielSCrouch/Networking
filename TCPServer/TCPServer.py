from socket import *
serverAddress = ('', 12000)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(1)
print('The Server is ready to receive...')
while 1:
    connectionSocket, addr = serverSocket.accept() #Handshake with client
    data = connectionSocket.recv(1024)
    modifiedData = data.upper()
    connectionSocket.send(modifiedData)
    print("Data sent")
    connectionSocket.close()
