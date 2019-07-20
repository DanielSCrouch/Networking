from socket import *
from time import sleep
import random

# setup UDP Sever
serverAddress = ('localhost', 4000)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

print("The Server is ready to receive....")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    # sleep(random.choice([1.0]))
    serverSocket.sendto(message, clientAddress)
    print("Message returned.")
