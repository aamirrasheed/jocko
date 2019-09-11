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


