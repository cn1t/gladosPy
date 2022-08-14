import asyncio

from imutils import paths
import face_recognition
import pickle
import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
from centralCore import glados_speak, record_audio

cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))

def headshotCam():
	glados_speak("Bitte sage deinen Namen laut und deutlich.")

	hMode = True
	hMode2 = False
	nameValid = False
	enteredName = "Error"
	glados_speak("Bitte sage deinen Namen laut und deutlich.")
	while hMode == True:
		voice_data = record_audio()

		if voice_data != None:

			glados_speak(f"Ist der Name: {voice_data} richtig? Bitte wiederhole deinen Namen.")
			enteredName = voice_data
			hMode = False
			hMode2 = True
	glados_speak("Bitte sage deinen Namen laut und deutlich.")
	while hMode2 == True:
		voice_data = record_audio()

		if voice_data != None:
			if enteredName != voice_data:
				glados_speak("Dieser Name entspricht nicht dem vorher genannten Namen.")
				glados_speak("Gesichtsregistrierung wird geschlossen.")
				hMode2 = False
			else:
				glados_speak(f"Der folgende Name wurde festgelegt: {enteredName}")
				hMode2 = False
				nameValid = True

	if nameValid == True:
		name = enteredName
		img_counter = 0

		glados_speak("Ich werde jetzt 10 Fotos aufnehmen. Bitte nutze unterschiedliche Gesichtsausdrücke oder Winkel.")
		asyncio.sleep(2)

		while True:
			for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
				image = frame.array
				cv2.imshow("Press Space to take a photo", image)
				rawCapture.truncate(0)

				for i in range(10):
					glados_speak("3")
					glados_speak("2")
					glados_speak("1")

					img_name = "dataset/" + name + "/image_{}.jpg".format(img_counter)
					cv2.imwrite(img_name, image)
					print("{} written!".format(img_name))
					img_counter += 1
					asyncio.sleep(2)
				break

		cv2.destroyAllWindows()
		glados_speak("Alle Fotos wurden aufgenommen.")


def trainModel():
	print("[INFO-intelligenceCore] Started processing faces...")
	imagePaths = list(paths.list_images("dataset"))

	knownEncodings = []
	knownNames = []

	for (i, imagePath) in enumerate(imagePaths):
		print("[INFO-intelligenceCore] Processing image {}/{}".format(i + 1, len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb, model="hog")

		encodings = face_recognition.face_encodings(rgb, boxes)

		for encoding in encodings:
			knownEncodings.append(encoding)
			knownNames.append(name)

	print("[INFO-intelligenceCore] Serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open("encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()