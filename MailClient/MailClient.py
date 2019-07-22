from socket import *
import base64
import time
import ssl

# Define client mail server
mailServer = ('smtp.gmail.com', 587) #google TLS option
username = 'duart2838@gmail.com'
password = 'bigcat!!!'
recipient = 'd_crouch@outlook.com'
### Google setup:
### Requires TLS (and associated port 587)
### Enable enabled IMAP in gmail ??? not sure if necessary
### Enable 'less secure app access'
### Check inbox for emails identifying blocked communications

global SOCKET

def send(msg):
    """Send string message to server in bytes format"""
    if type(msg) == str:
        SOCKET.send(msg.encode())
    else:
        SOCKET.send(msg)

def receive():
    """Return client server message and convert to string"""
    recv = SOCKET.recv(1024)
    return recv.decode()

# 0) Connect to mail server
SOCKET = socket(AF_INET, SOCK_STREAM) # Setup TCP Client Socket
SOCKET.settimeout(10)                 # Set time-out to 10 seconds
SOCKET.connect(mailServer)            # Connect to client mail server
rmsg = receive()
if rmsg[:3]=='220':
    print('\nConnection success.')
else:
    print('Error')
print('Response message: ', rmsg)

# 1) HELO command
msg = 'HELO server\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='250':
    print('Helo success.')
else:
    print('Error')
print('Response message: ', rmsg)

# 2) Initialise TLS (GMail uses requires TLS on port 587)
msg = 'STARTTLS\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='220':
    print('Start TLS success.')
else:
    print('Error')
print('Response message: ', rmsg)
SOCKET = ssl.wrap_socket(SOCKET, ssl_version=ssl.PROTOCOL_TLS)

# 3) Mail Server Authorisation
login = '\x00'+username+'\x00'+password
loginBytes = login.encode()
loginBase64 = base64.b64encode(loginBytes)
msg = 'AUTH PLAIN '.encode()+loginBase64+'\r\n'.encode()
send(msg)
rmsg = receive()
if rmsg[:3]=='235':
    print('Authorisation success.')
else:
    print('Error')
print('Response message: ', rmsg)

# 4) MAIL FROM Command
msg = 'MAIL FROM: <' + username + '>\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='250':
    print('Mail From success.')
else:
    print('Error')
print('Response message: ', rmsg)

# 5) RCPT TO Command
msg = 'RCPT TO: <' + recipient + '>\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='250':
    print('Receipt To success.')
else:
    print('Error')
print('Response message: ', rmsg)

# Initialise DATA send
msg = 'DATA \r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='354':
    print('Data initialise success.')
else:
    print('Error')
print('Response message: ', rmsg)

# Send Subject
msg = 'SUBJECT: Hello, World\r\n'
send(msg)

# Send To
msg = 'TO: ' + recipient + '\r\n'
send(msg)

# Send Body
msg = 'Tell me and I forget. Show me and I remember. Involve me and I understand.'
msg += '\n Chinese proverb  \r\n'
send(msg)

# End of data
msg = '.\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='250':
    print('End data success.')
else:
    print('Error')
print('Response message: ', rmsg)

# Send QUIT
msg = 'QUIT\r\n'
send(msg)
rmsg = receive()
if rmsg[:3]=='221':
    print('Quit command success.')
else:
    print('Error')
print('Response message: ', rmsg)

# Close socket
SOCKET.close()
print('Socket closed.\n')
