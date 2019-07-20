import re
from socket import *
from datetime import datetime

def pingServer(serverAddress, clientSocket):
    """Send ping to server and wait 1 second for response"""

    # Send message
    dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dateTimeBytes =  dateTime.encode()
    clientSocket.sendto(dateTimeBytes, serverAddress)

    # Wait for response
    try:
        # Receive response
        modifiedData, serverAddress = clientSocket.recvfrom(2048)
        modifiedData = modifiedData.decode('utf-8')

        # Calculate Round Trip Time (RTT)
        dateTimeSent = datetime.strptime(modifiedData, '%Y-%m-%d %H:%M:%S')
        dateTime = datetime.now()
        timeElapsed = dateTime - dateTimeSent
        return timeElapsed.total_seconds().__str__()

    except OSError:
        clientSocket.close()
        return "timeout"

for i in range(10):
    serverAddress = ('localhost', 4000)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(1)
    print(i, ": ", pingServer(serverAddress, clientSocket))
