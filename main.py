from voice import speak, listen, process_command

def run_jarvis():
    active = True
    speak("JARVIS is now online, sir. How may I assist you?")
    while active:
        command = listen()
        if command:
            active = process_command(command)

if __name__ == "__main__":
    run_jarvis()