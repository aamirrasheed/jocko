import socket

from rpi_ip_addr import get
host = get()
port = 12345
print(host)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,port))
    while True:
        x = input('Type data to send to server\n')
        x = x.encode('utf-8')
        s.sendall(x)
        print("Sent ", x, " to server")
        data = s.recv(1024)
        data = data.decode('utf-8')
        data = str(data)
        print("Received ", data, " from server")
