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
from personalityCores.factCore import randomFact, weatherFrog

# 246 character messages max

r = sr.Recognizer()
r.energy_threshold = 4000
file = "configFiles/userData.ini"
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
    path = os.path.join('''C:\\Users\\Mathis\\PycharmProjects\\gladosPy\\soundFiles''', audio_file)
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

while True: #Run glados
    voice_data = record_audio()
    respond(voice_data)