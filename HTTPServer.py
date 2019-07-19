# Internal 0eth ip
# http://192.168.1.3/HelloWorld.html

#import socket module
from socket import *
serverPort=3080
serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("Web server listening on port:", serverPort)

#Establish the connection
while True:
    print("\nAwaiting client... \n")
    connectionSocket, addr = serverSocket.accept()
    print("Client connected, address: ", addr)
    #Handle client message
    try:
        message = connectionSocket.recv(1024)
        messageStr = message.decode("utf-8")
        print("Message Header: ", messageStr.split()[0], ' ', messageStr.split()[1])

        filename = messageStr.split()[1]
        f = open(filename[1:])
        outputData = f.read()
        outputDataBytes = outputData.encode()
        #Send one HTTP header line into socket
        connectionSocket.send('\nHTTP/1.1 200 OK\n\n'.encode())
        connectionSocket.send(outputDataBytes)
        #Send the content of the requested file to the client
        # for i in range(0, len(outputdata)):
        #     connectionSocket.send(outputdata[i])
        print("Data sent.")
        connectionSocket.close()
        print("Connection closed.")
    except IOError:
        #Send response message for file not found
        connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
        connectionSocket.send('\nHTTP/1.1 404 Not Found\n\n'.encode())
