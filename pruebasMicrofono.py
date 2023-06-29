import speech_recognition as sr
import pyttsx3




def listen():
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language='es-ES')
            rec = rec.lower()
        print(rec)
        return rec
    except Exception as e:
        print(e)

from gtts import gTTS
from playsound import playsound
from os import remove
def speak2(text):
    tts = gTTS(text, lang='es-es')
    tts.save('pruebas.mp3')
    playsound("pruebas.mp3")
    remove("pruebas.mp3")

sound = speak2(listen())

