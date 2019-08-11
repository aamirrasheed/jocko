import socket
import os

import rpi_ip_addr

s = socket.socket(socket.AF_INET, )
host = rpi_ip_addr.get()
port = 12345
s.connect((host,port))
print(s.recv(1024))
s.close()

