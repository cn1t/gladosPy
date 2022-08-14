import RPi.GPIO as GPIO
import time

GPIO_TRIGGER = 18
GPIO_ECHO = 24


GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setmode(GPIO.BCM)


def getDistance():
    """
    Description:
        Recieve distance data from the ultrasound sensor,
        used to detect if something is directly in front of the robot.

    Returns:
        - distance: Distance in cm with 1 decimal
    """

    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    startTime = time.time()
    stopTime = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        startTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stopTime = time.time()

    timeElapsed = stopTime - startTime
    distance = round((timeElapsed * 34300) / 2) # Multiply with speed of sound (34300 cm/s) and divide with 2 (forward and backward) and then round to 1 decimal.

    print(f"[INFO-spaceCore/getDistance] A distance of '{distance}'cm has been returned.")
    return distance