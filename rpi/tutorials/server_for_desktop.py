import socket
from get_local_ip import get

host = get()
port = 12345
print("Retrieved internal ip: ", host)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host,port))
    s.listen(5)
    connection, address = s.accept()
    with connection:
        print('Connected by', address)
        while True:
            data = connection.recv(1024)
            if not data:
                break
            data = data.decode('utf-8')
            data = str(data)
            print("Received ", data, " from client. Sending it back...")
            data = "Client sent: " + data
            data = data.encode('utf-8')
            connection.sendall(data)

