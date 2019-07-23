# python3 ProxyServer.py http://localhost:8888/www.google.com

from socket import *
import sys

if len(sys.argv) <= 1:
       print('Usage: "python3 ProxyServer.py server_ip"\n\
       server_ip: IP Address of Proxy Server')
       sys.exit(2)

# Create a server socket, bind it to a port and start listening tcpSerSock = socket(AF_INET, SOCK_STREAM)
serverAddress = ('localhost', 3001)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(1)
print('Ready to serve...')

#####################################################
while True:
    tcpCliSock, addr = serverSocket.accept() #Handshake with client
    print('Received a connection from: ', addr)
    message = serverSocket.recv(1024)
    print('Message received: \n', message)
    # Extract the filename from given message and print
    filename = message.split()[1].partition("/")[2]
    print('Filename: ', filename)
    fileExist = "false"
    filetouse = "/" + filename
    print(filetouse)
    try:
    # Check wether the file exist in the cache
        f = open(filetouse[1:], "r")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        # add headers optional
        tcpCliSock.send("Content-Type:text/html\r\n")
        tcpCliSock.send("\n\n" + outputdata) # Check functions as expected ???
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            hostAddress = ('localhost', 80)
            clientSocket = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace('www.','',1)
            print('Host Name: ', hostn)
            try:
                clientSocket.connect(hostAddress)
                # Create a temporary file on this sicket and ask port 80 for the file requested by the cient
                fileobj = clientSocket.makefile('r', 0)
                fileobj.write("GET "+"http://" + filename + "HTTP/1.0\n\n")
                # Read the response into buffer
                clientSocket.send(fileobj)
                buffer = clientSocket.recv(2048)
                tcpCliSock.send(buffer)
            except:
                print('Illegal request')

        else:
            # HTTP response message for file not found
            continue
    clientSocket.close()
serverSocket.close()
