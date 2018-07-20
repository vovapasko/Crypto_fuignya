import socket  # Import socket module
from UrlBuilder import *
import threading
import time


def client_manage(c, i):
    data = get_all_data()
    send_data = ["id: {}, name: {}, symbol: {}".format(item['id'], item['name'], item['symbol']) for item in
                 data['data']]
    str_data = '\n'.join(send_data)
    send_str = "Thank you for connecting\nData: " + str_data
    c.send(send_str.encode())
    while True:
        from_client = c.recv(1024).decode()
        time.sleep(2)
        if not from_client:
            print('End work thread', i)
            c.close()
            break
        else:
            print('-----------\nThread #', i, 'got:', from_client, '\n-------------')


s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
print(host)
port = 12345  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port

s.listen(5)
i = 0
while True:
    print('server wait for client connection.')
    client, addr = s.accept()  # Establish connection with client.
    i += 1

    t = threading.Thread(target=client_manage, args=(client, i), name=i)
    t.daemon = True
    t.start()

    print('\nGot connection from', addr)
    print('Work thread', t.name, '\n')
