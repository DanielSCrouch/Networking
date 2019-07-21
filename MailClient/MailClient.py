from socket import *
import base64
import time
import ssl
from ssl import SSLContext

### Code functional - needs cleaning 


# Define client mail server
mailServer = ('smtp.gmail.com', 587) #google TLS option
username = 'duart2838@gmail.com'
password = 'bigcat!!!'
### Google setup:
### Requires TLS (and associated port 587)
### Enable enabled IMAP in gmail ??? not sure if necessary
### Enable 'less secure app access'
### Check inbox for emails identifying blocked communications

# Connect to mail server
clientSocket = socket(AF_INET, SOCK_STREAM) # Setup TCP Client Socket
clientSocket.settimeout(10)                 # Set time-out to 10 seconds
clientSocket.connect(mailServer)            # Connect to client mail server
recv = clientSocket.recv(1024)              # Print Response
recv = recv.decode()
print("Connection request response message: ", recv)

# HELO command
HELOcommand = "HELO Alice\r\n"
clientSocket.send(HELOcommand.encode())
recv = clientSocket.recv(1024)
recv = recv.decode()
print("HELO response message: ", recv)

# Initialise TLS
command = "STARTTLS\r\n"
clientSocket.send(command.encode())
sock = clientSocket
recv = clientSocket.recv(1024)
recv = recv.decode()
print("STARTTLS response message: ", recv)
# Update socket (add error check)
clientTSLSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)

# Authorisation
# login = "\x00"+username+"\x00"+password
login = '\x00'+username+'\x00'+password
loginBytes = login.encode()
loginBase64 = base64.b64encode(loginBytes)
command = "AUTH PLAIN ".encode()+loginBase64+"\r\n".encode()
clientTSLSocket.send(command)
recv = clientTSLSocket.recv(1024)
recv = recv.decode()
print("AUTH response message: ", recv)

# MAIL FROM Command
mailFrom = "MAIL FROM: <" + username + ">\r\n"
clientTSLSocket.send(mailFrom.encode())
recv = clientTSLSocket.recv(1024)
recv = recv.decode()
print("After MAIL FROM command: "+recv)

# RCPT TO Command
rcptTo = "RCPT TO:<d_crouch@outlook.com>\r\n"
clientTSLSocket.send(rcptTo.encode())
recv3 = clientTSLSocket.recv(1024)
recv3 = recv3.decode()
print("After RCPT TO command: "+recv3)

# Send DATA
command = "DATA\r\n"
clientTSLSocket.send(command.encode())
recv = clientTSLSocket.recv(1024)
recv = recv.decode()
print("Data response message: ", recv)

# Send Subject
subject = 'test subject'
command = "SUBJECT: " + subject + "\r\n"
clientTSLSocket.send(command.encode())

# Send To
subject = 'someone'
command = "TO: " + subject + "\r\n"
clientTSLSocket.send(command.encode())

# Send Body
body = 'test body'
command = "\r\n I love computer networks \r\n"
clientTSLSocket.send(command.encode())

# Send endobj
endmsg = ".\r\n"
command = endmsg
clientTSLSocket.send(command.encode())
recv = clientTSLSocket.recv(2014)
recv = recv.decode()
print("End response message:", recv)

# Send QUIT
quitmsg = "QUIT\r\n"
command = quitmsg
clientTSLSocket.send(command.encode())
recv = clientTSLSocket.recv(2014)
recv = recv.decode()
print("QUIT response message:", recv)

clientTSLSocket.close()
