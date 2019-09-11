import socket
import subprocess
import re

import RPi.GPIO as GPIO

# constants
OUTPUT_PINS = [33, 11, 13, 32, 16, 18]
ENABLE_A_PIN = OUTPUT_PINS[3]
INPUT_1_A_PIN = OUTPUT_PINS[4]
INPUT_2_A_PIN = OUTPUT_PINS[5]

ENABLE_B_PIN = OUTPUT_PINS[0]
INPUT_3_B_PIN = OUTPUT_PINS[1]
INPUT_4_B_PIN = OUTPUT_PINS[2]

PWM_FREQ = 1000

class MotorController():
    def __init__(self, speed=80):
        # cleanup pins from previous runs
        GPIO.cleanup()

        # setup pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(OUTPUT_PINS, GPIO.OUT)

        self.motor_a = GPIO.PWM(ENABLE_A_PIN, PWM_FREQ)
        self.motor_a.start(speed)
        self.motor_b = GPIO.PWM(ENABLE_B_PIN, PWM_FREQ)
        self.motor_b.start(speed)

    def turnleft(self):
        # motor A
        GPIO.output(INPUT_1_A_PIN, GPIO.HIGH)
        GPIO.output(INPUT_2_A_PIN, GPIO.LOW)
        # motor B
        GPIO.output(INPUT_3_B_PIN, GPIO.LOW)
        GPIO.output(INPUT_4_B_PIN, GPIO.HIGH)

    def turnright(self):
        # motor A
        GPIO.output(INPUT_1_A_PIN, GPIO.LOW)
        GPIO.output(INPUT_2_A_PIN, GPIO.HIGH)
        # motor B
        GPIO.output(INPUT_3_B_PIN, GPIO.HIGH)
        GPIO.output(INPUT_4_B_PIN, GPIO.LOW)

    def goforward(self):
        # motor A
        GPIO.output(INPUT_1_A_PIN, GPIO.HIGH)
        GPIO.output(INPUT_2_A_PIN, GPIO.LOW)
        # motor B
        GPIO.output(INPUT_3_B_PIN, GPIO.HIGH)
        GPIO.output(INPUT_4_B_PIN, GPIO.LOW)

    def gobackward(self):
        # motor A
        GPIO.output(INPUT_1_A_PIN, GPIO.LOW)
        GPIO.output(INPUT_2_A_PIN, GPIO.HIGH)
        # motor B
        GPIO.output(INPUT_3_B_PIN, GPIO.LOW)
        GPIO.output(INPUT_4_B_PIN, GPIO.HIGH)

    def stop(self):
        # motor A
        GPIO.output(INPUT_1_A_PIN, GPIO.LOW)
        GPIO.output(INPUT_2_A_PIN, GPIO.LOW)
        # motor B
        GPIO.output(INPUT_3_B_PIN, GPIO.LOW)
        GPIO.output(INPUT_4_B_PIN, GPIO.LOW)
        
    def setspeed(self, speed):
        pass

    def shutdown(self):
        self.motor_a.stop()
        self.motor_b.stop()
        GPIO.cleanup()


class ServerController():
    def __init__(self, host, port, controller):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controller = controller
        self.controller.stop()
                                        
    def run(self):
        self.s.bind((host,port))
        self.s.listen(5)
        print("Listening from ", self.host, " on port ", self.port)
        connection, address = self.s.accept()
        with connection:
            print('Connected by', address)
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.decode('utf-8')
                data = str(data)
                print("Received \'", data, "\' from client.")
                if data == 'left':
                    print('Turning left')
                    self.controller.turnleft()
                elif data == 'right':
                    print('Turning right')
                    self.controller.turnright()
                elif data == 'forward':
                    print('moving forward')
                    self.controller.goforward()
                elif data == 'backward':
                    print('moving backward')
                    self.controller.gobackward()
                elif data == 'stop':
                    print('stopping')
                    self.controller.stop()
                else:
                    print("Got incorrect command: \'", data, "\' from client")

        self.shutdown()

    def shutdown(self):
        self.controller.shutdown()
        self.s.close()

"""
Retrieves IP address of this RPI using command line
"""
cmd = "ifconfig | grep -A 1 wlan0 | grep 'inet addr' | awk -F ':' '{print $2}' | awk '{print $1}'"
regex_match_IPv4 = "^(\d{1,3}\.){3}\d{1,3}$"
no_rpi_exception_message = "Couldn't find aamirpi on LAN"
regex_exception_message = "Couldn't get IP address of raspberry pi - {0} isn't a valid IPv4 address"

def get_local_ip():
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

controller = MotorController()
host = get_local_ip()
port = 12345
server = ServerController(host, port, controller)
server.run()
