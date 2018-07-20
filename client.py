import socket  # Import socket module
import time
import json

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.

s.connect((host, port))
print(s.recv(646010).decode())
send_data = json.dumps({'id': 1})
s.send(send_data.encode())

print('----\ndone')

# s.close()  # Close the socket when done
