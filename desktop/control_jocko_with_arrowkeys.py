import socket

class Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.s.connect((self.host, self.port))
        except:
            print("Couldn't connect to server")

    def send(self, string_message):
        byte_message = string_message.encode('utf-8')
        self.s.sendall(byte_message)
        print("Sent ", byte_message, " to server")
        data = self.s.recv(1024)
        data = data.decode('utf-8')
        data = str(data)
        print("Received ", data, " from server")

    def shutdown(self):
        self.s.close()

import subprocess
import re

# constants
cmd = "arp -a | grep aamirpi | awk -F '(' '{print $2}' | awk -F ')' '{print $1}'"
regex_match_IPv4 = "^(\d{1,3}\.){3}\d{1,3}$"
no_rpi_exception_message = "Couldn't find aamirpi on LAN"
regex_exception_message = "Couldn't get IP address of raspberry pi - {0} isn't a valid IPv4 address"

def get_jocko_ip():
    # execute command
    task = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = task.stdout.read()
    if output == '':
        raise Exception(no_rpi_exception_message)

    # clean output
    output = output.decode('utf-8')
    output = str(output)
    output = output.replace('\n','')
    
    # verify that output is IPv4 address with regex
    match = re.search(regex_match_IPv4, output)
    if match:
        return output
    else:
        raise Exception(regex_exception_message.format(output))

host = get_jocko_ip()
port = 12345
client = Client(host, port)
client.connect()
client.send("Client sending hey!")

import pyglet
from pyglet.window import key

window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        client.send('left')
    elif symbol == key.RIGHT:
        client.send('right')
    elif symbol == key.UP:
        client.send('up')
    elif symbol == key.DOWN:
        client.send('down')

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.LEFT:
        client.send('Left unpressed.')
    elif symbol == key.RIGHT:
        client.send('Right unpressed.')
    elif symbol == key.UP:
        client.send('Up unpressed.')
    elif symbol == key.DOWN:
        client.send('Down unpressed')

pyglet.app.run()
client.shutdown()

