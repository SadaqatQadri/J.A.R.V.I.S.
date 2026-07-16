import pyttsx3
import speech_recognition as sr
import os
from weather import get_weather
from news import get_news
from spotify import play_song, play_playlist, pause, resume, skip, previous, volume, current_track
import gui_bridge
import brain
import time

def speak(text):
    engine = pyttsx3.init()
    gui_bridge.update_status("speaking", text)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.03)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening, sir...")
        gui_bridge.update_status("listening", "Listening sir...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            command = r.recognize_google(audio)
            print("You said: " + command)
            return command
        except sr.UnknownValueError:
            speak("I didn't quite catch that, sir.")
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable, sir.")
            return ""
        except sr.WaitTimeoutError:
            speak("I didn't hear anything, sir.")
            return ""

def process_command(command):
    command_lower = command.lower()

    if "shut down" in command or "goodbye" in command_lower:
        speak("Goodbye, sir.")
        return False
    
    result = brain.think(command)
    speak(result)

    if "news" in command_lower:
        gui_bridge.show_news(result)

    return True

if __name__ == "__main__":

    active = True
    speak("JARVIS is now online, sir. How may I assist you?")
    while active:
        command = listen()
        if command:
            active = process_command(command)

