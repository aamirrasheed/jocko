import socket
import os
get_rpi_address_cmd = ''

s = socket.socket()
host = os.system(get_rpi_address_cmd)
port = get_rpi_port()
s.bind((host,port))

s.listen(5)
while True:



