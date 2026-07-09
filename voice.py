import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening, sir...")
        r.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
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
    command = command.lower()

    if "hear me" in command or "hello" in command:
        speak("Yes sir, I can hear you loud and clear.")
    elif "your name" in command:
        speak("I am  JARVIS, your personal assistant")
    elif "how are you" in command:
        speak("Running at full capacity, sir.")
    elif "stop" in command or "exit" in command:
        speak("Goodbye, sir.")
        return False
    else:
        speak("I heard you say: " + command + ", but I don't know how to respond to that yet, sir.")
        
    return True    

active = True
speak("JARVIS is now online, sir. How may I assist you?")
while active:
    command = listen()
    if command:
        active = process_command(command)

