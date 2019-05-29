import RPi.GPIO as GPIO
import time
import signal
import sys
from firebase import firebase

firebase = firebase.FirebaseApplication(
    "https://smart-iot-android.firebaseio.com/")

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 23
pinEcho = 18


def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

while True:
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 1ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)

    # save start time
    while 0 == GPIO.input(pinEcho):
        startTime = time.time()

    # save time of arrival
    while 1 == GPIO.input(pinEcho):
        stopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = stopTime-startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = TimeElapsed/0.000058

    print('Dist : {} cm'.format(distance))
    result = firebase.put('', "distance", '%.2f cm' % distance)
    print(result)
    # time.sleep(1)

GPIO.cleanup()
