import socket  # Import socket module
import time
import json

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.

s.connect((host, port))
print(s.recv(646010).decode())
send_data = json.dumps({'look': True, 'id': [1, 2, 3], 'open': True})
s.send(send_data.encode())
print('--------1')
print(s.recv(5000).decode())
print('--------2')
print(s.recv(5000).decode())
print('--------3')
print(s.recv(5000).decode())

print('----\ndone')

# s.close()  # Close the socket when done
