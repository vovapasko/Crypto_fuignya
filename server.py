import socket  # Import socket module
from UrlBuilder import *

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
print(host)
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)
clients = []
print('Now wait for client connection.')
while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    data = get_all_data()
    send_data = ["id: {}, name: {}, symbol: {}".format(item['id'], item['name'], item['symbol']) for item in
                 data['data']]
    str_data = '\n'.join(send_data)
    send_str = "Thank you for connecting\nData: " + str_data
    c.send(send_str.encode())
    print(c.recv(1024).decode())
    c.close()

"""
print('----')
i = 0
for c, addr in clients:
    print("It's connection from", addr)
    i += 1
    message = 'hello again client number {}'.format(i)
    c.send(message.encode())
"""
