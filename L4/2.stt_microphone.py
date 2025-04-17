import speech_recognition as sr
import os

#obtain audio from the microphone
r=sr.Recognizer() 

with sr.Microphone() as source:
    print("Please wait. Calibrating microphone...") 
    #listen for 1 seconds and create the ambient noise energy level 
    r.adjust_for_ambient_noise(source, duration=1) 
    print("Say something!")
    audio=r.listen(source)

# recognize speech using Whisper API
OPENAI_API_KEY = "API Key"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
try:
    print(f"OpenAI Whisper API thinks you said {r.recognize_openai(audio)}")
except sr.RequestError as e:
    print(f"Could not request results from OpenAI Whisper API; {e}")

