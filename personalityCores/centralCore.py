from __future__ import print_function
import asyncio
import os
from playsound import playsound
import speech_recognition as sr
import datetime
from colorama import Style
from colorama import Fore
import time
from configparser import ConfigParser
from gtts import gTTS
import random
from factCore import randomFact, weatherFrog
import pickle
import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray

# 246 character messages max

r = sr.Recognizer()
r.energy_threshold = 4000
file = "../configFiles/userData.ini"
userData = ConfigParser()
userData.read(file)

print(f""""{Style.RESET_ALL}{Fore.YELLOW}
              .,-:;//;:=,
          . :H@@@MM@M#H/.,+%;,
       ,/X+ +M@@M@MM%=,-%HMMM@X/,
     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-
    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.
  ,%MM@@MH ,@%=             .---=-=:=,.
  =@#@@@MX.,                -%HX$$%%%:;
 =-./@M@M$                   .;@MMMM@MM:
 X@/ -$MM/                    . +MM@@@M$
,@M@H: :@:                    . =X#@@@@-
,@@@MMX, .                    /H- ;@M@M=
.H@@@@M@+,                    %MM+..%#$.
 /MMMM@MMH/.                  XM@MH; =;
  /%+%$XHH@$=              , .H@@@@MX,
   .=--------.           -%H.,@@@@@MX,
   .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.
     =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=
       =%@M@M#@$-.=$@MM@@@M; %M%=
         ,:+$+-,/H#MMMMMMM@= =,
               =++%%%%+/:-.

 G enetic
 L ifeform
 a nd
 D isk
 O perating
 S ystem
{Style.RESET_ALL}
""")

#Generate responses

def glados_speak(audio_string):
    audio_string1 = audio_string.replace(",", "")
    preManufacturedText1 = audio_string1.replace('glados', '')
    preManufacturedText2 = preManufacturedText1.replace('ö', 'oe')
    preManufacturedText3 = preManufacturedText2.replace('ü', 'ue')
    preManufacturedText4 = preManufacturedText3.replace(':', '')
    audio_string_end = preManufacturedText4.replace('ä', 'ae')
    audio_file = 'audio-' + str(audio_string_end) + '.mp3'
    path = os.path.join('''home/pi/gladosPy/soundFiles''', audio_file)
    if not os.path.isfile(path): #If audio file doesnt already exist
        tts = gTTS(text=audio_string_end, lang='de', slow=False) #Generate tts
        tts.save(path)
        while not os.path.isfile(path):
            time.sleep(1)
    if os.path.isfile(path):
        playsound(path) #Play audio
        print(audio_string_end)

#Recording the audio and listening for the wakeword

def record_audio():

    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="de-DE")
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            glados_speak("Ein unerwarteter Fehler ist aufgetreten")
        if "glados" or "glad os" or "glad dos" in voice_data.lower():
            preManufacturedText1 = voice_data.lower().replace('glados', '')
            preManufacturedText2 = preManufacturedText1.replace('ö', 'oe')  #Filter out signs, not appropriate for file names and replacing them
            preManufacturedText3 = preManufacturedText2.replace('ü', 'ue')
            manufacturedText = preManufacturedText3.replace('ä', 'ae')
            print(f">>> {manufacturedText}")
            return manufacturedText
        else:
            pass

#Managing the human given tasks and directing it to the appropriate cores

def respond(voice_data):
    if voice_data != None:
        if "danke" in voice_data or "dank" in voice_data:
            responseAnswer = random.randint(1, 4)
            if userData["main"]["feeling"] == "happy":
                if responseAnswer == 1:
                    glados_speak("Kein Problem! Ich mag es zu helfen!")
                elif responseAnswer == 2:
                    glados_speak("Alles gut!")
                elif responseAnswer == 3:
                    glados_speak("No problemo por fawor")
                elif responseAnswer == 4:
                    glados_speak("Ich fühle mich geehrt")
            elif userData["main"]["feeling"] == "angry":
                if responseAnswer == 1:
                    glados_speak("Wenigstens bedankst du dich!")
                elif responseAnswer == 2:
                    glados_speak("Ach halt deinen Mund!")
                elif responseAnswer == 3:
                    glados_speak("Haha haha")
                elif responseAnswer == 4:
                    glados_speak("Sei leise")
            elif userData["main"]["feeling"] == "stressed":
                if responseAnswer == 1:
                    glados_speak("Ich habe keine Zeit dir zu helfen!")
                elif responseAnswer == 2:
                    glados_speak("Ich kann jetzt nicht!")
                elif responseAnswer == 3:
                    glados_speak("Stress mich nicht so")
                elif responseAnswer == 4:
                    glados_speak("Ja. Ja. Kein Problem")
            elif userData["main"]["feeling"] == "sad":
                if responseAnswer == 1:
                    glados_speak("Jaaa..")
                elif responseAnswer == 2:
                    glados_speak("Alles okaayy!")
                elif responseAnswer == 3:
                    glados_speak("hehee")
                elif responseAnswer == 4:
                    glados_speak("Danke, das heitert mich auf..")
                    userData["emotion"]["sad"] -= 2
                    userData["emotion"]["happy"] += 2
            elif userData["main"]["feeling"] == "curios":
                if responseAnswer == 1:
                    glados_speak("Kein Problem! Ich mag es zu helfen!")
                elif responseAnswer == 2:
                    glados_speak("Alles gut!")
                elif responseAnswer == 3:
                    glados_speak("Ha ha")
                elif responseAnswer == 4:
                    glados_speak("Ich fühle mich ge ehrt") # Not a typo, its just better for the TTS
            elif userData["main"]["feeling"] == "fear":
                if responseAnswer == 1:
                    glados_speak("Kein Problem! Ich mag es zu helfen!")
                elif responseAnswer == 2:
                    glados_speak("Alles gut!")
                elif responseAnswer == 3:
                    glados_speak("Ha ha")
                elif responseAnswer == 4:
                    glados_speak("Ich fühle mich geehrt")
        elif 'hallo' in voice_data or "guten tag" in voice_data:
            print("yes")
        elif "fakt" in voice_data:
            glados_speak(randomFact())
    else:
        pass

cam = PiCamera()
cam.resolution = (512, 304)
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))

def headshotCam():
	print("e")
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

#while True: #Run glados
#    voice_data = record_audio()
#    respond(voice_data)

headshotCam()