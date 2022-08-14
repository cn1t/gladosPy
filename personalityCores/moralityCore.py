import RPi.GPIO as GPIO

ledPinGreen = 13
ledPinYellow = 5
ledPinRed = 6


GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPinGreen, GPIO.OUT)
GPIO.setup(ledPinYellow, GPIO.OUT)
GPIO.setup(ledPinRed, GPIO.OUT)


def changeLed(led: str, state: str):
    """
    Parameters:
        - led: ledPinGreen, ledPinYellow, ledPinRed
        - state: on, off

    Description:
        Changes the state of one of the leds in the 'emotion light'.
    """

    if state == "on":
        GPIO.output(led, GPIO.HIGH)
        print("Notification from: 'moralityCore-changeLed':\n"
              f"'{led}' has been turned on.")
    elif state == "off":
        GPIO.output(led, GPIO.LOW)
        print(f"[INFO-moralityCore/changeLed] '{led}' has been turned off.")
    else:
        print("Error in 'moralityCore-changeLed':\n"
              f"State: '{state}' is invalid. Valid states are: 'on' or 'off'.")