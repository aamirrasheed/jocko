import RPi.GPIO as GPIO

"""
Description:
This file describes a program for the Raspberry Pi Model 3b v1.2 to drive two 12V motors 
(MotorA, MotorB) with the L298N motor controller.

RPI Model 3b v1.2 Pinout Reference: https://pi4j.com/1.2/pins/model-3b-rev1.html (refer to inner numbers)

L298N Pinout Reference: https://i.pinimg.com/originals/b1/3a/d2/b13ad2c13e5c1ab897bafda0788c8802.jpg

WIRE CONFIGURATION - Raspberry PI to L298N Motor Controller:
Pin 11 to Input3
Pin 13 to Input4
Pin 16 to Input1
Pin 18 to Input2
Pin 32 to EnableA
Pin 33 to EnableB

"""

# constants
OUTPUT_PINS = [33, 11, 13, 32, 16, 18]
ENABLE_A_PIN = OUTPUT_PINS[3]
INPUT_1_A_PIN = OUTPUT_PINS[4]
INPUT_2_A_PIN = OUTPUT_PINS[5]

ENABLE_B_PIN = OUTPUT_PINS[0]
INPUT_3_B_PIN = OUTPUT_PINS[1]
INPUT_4_B_PIN = OUTPUT_PINS[2]

PWM_FREQ = 1000
PWM_DUTY_CYCLE_A = 80 # change to modify speed of motor A (0-100)
PWM_DUTY_CYCLE_B = 80  # change to modify speed of motor B (0-100)

ENABLE_PWM = True

# setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(OUTPUT_PINS, GPIO.OUT) 

def turnleft():
    # motor A
    GPIO.output(INPUT_1_A_PIN, GPIO.HIGH)
    GPIO.output(INPUT_2_A_PIN, GPIO.LOW)
    # motor B
    GPIO.output(INPUT_3_B_PIN, GPIO.LOW)
    GPIO.output(INPUT_4_B_PIN, GPIO.HIGH)

def turnright():
    # motor A
    GPIO.output(INPUT_1_A_PIN, GPIO.LOW)
    GPIO.output(INPUT_2_A_PIN, GPIO.HIGH)
    # motor B
    GPIO.output(INPUT_3_B_PIN, GPIO.HIGH)
    GPIO.output(INPUT_4_B_PIN, GPIO.LOW)

# specify PWM
if(ENABLE_PWM):
    motor_a = GPIO.PWM(ENABLE_A_PIN, PWM_FREQ)
    motor_a.start(PWM_DUTY_CYCLE_A)
    motor_b = GPIO.PWM(ENABLE_B_PIN, PWM_FREQ)
    motor_b.start(PWM_DUTY_CYCLE_B)
else:
    GPIO.output(ENABLE_A_PIN, GPIO.LOW)
    GPIO.output(ENABLE_B_PIN, GPIO.LOW)


# loop while waiting for entry from user
turnleft()
input("Press Enter to turn right")
turnright()
input("Press Enter to stop")

# close out pins
if(ENABLE_PWM):
    motor_a.stop()
    motor_b.stop()
GPIO.cleanup()

