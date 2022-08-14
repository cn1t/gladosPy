from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

pigpio_factory = PiGPIOFactory()
headServo = Servo(12, pin_factory=pigpio_factory)
elbowServo = Servo(16, pin_factory=pigpio_factory)
shoulderServo = Servo(20, pin_factory=pigpio_factory)
turnServo = Servo(21, pin_factory=pigpio_factory)

def resetServo(servoChoice: str):
	"""
	Parameters:
		- servoChoice: headServo, elbowServo, shoulderServo, turnServo

	Description:
		Reset the given servo to the 'mid' position.
	"""

	servoChoice.mid()
	print(f"[INFO-adventureCore/resetServo] '{servoChoice}' has been reset.")

def moveServo(servoChoice: str, pos: int):
	"""
	Parameters:
		- servoChoice: headServo, elbowServo, shoulderServo, turnServo
		- pos: The servo position, from -1 to 1

	Description:
		Move the given servo to the given position.
	"""

	servoChoice.value = pos
	print(f"[INFO-adventureCore/moveServo] '{servoChoice}' has been moved to position: '{pos}'.")