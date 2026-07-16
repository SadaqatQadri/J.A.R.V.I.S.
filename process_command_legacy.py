# Original rules-based command processor, replaced by brain.py (Groq LLM tool) on 15-07-2026

def process_command(command):
    command = command.lower()

    if "hear me" in command or "hello" in command:
        speak("Yes sir, I can hear you loud and clear.")
    elif "your name" in command:
        speak("I am  JARVIS, your personal assistant")
    elif "how are you" in command:
        speak("Running at full capacity, sir.")

    elif "weather" in command:
        if " in " in command:
            city = command.split("in")[-1].strip()
        else:
            city = "karachi"
        result = get_weather(city)
        speak(result)

    elif "news" in command:
        result = get_news()
        speak(result)
        gui_bridge.show_news(result)

    elif "playlist" in command:
        playlist_name = command.replace("play playlist", "").replace("playlist", "").strip()
        result = play_playlist(playlist_name)
        speak(result)

    elif "play" in command:
        song_name = command.replace("jarvis", "").replace("play", "").strip()
        song_name = " ".join(song_name.split()) 
        result = play_song(song_name)
        speak(result)

    elif "pause" in command or "stop the music" in command:
        result = pause()
        speak(result)

    elif "resume" in command or "unpause" in command:
        result = resume()
        speak(result)

    elif "skip" in command or "next" in command:
        result = skip()
        speak(result)

    elif "previous" in command or "go back" in command:
        result = previous()
        speak(result)

    elif "current song" in command or "what's playing" in command:
        result = current_track()
        speak(result)
    
    elif "volume" in command:
        words = command.split()
        number = None
        for word in words:
            if word.isdigit():
                number = int(word)
                break
        if number is not None:
            result = volume(number)
            speak(result)
        else:
            speak("What volume would you like, sir?")

    elif "shut down" in command or "goodbye" in command:
        speak("Goodbye, sir.")
        return False
    else:
        speak("I heard you say: " + command + ", but I don't know how to respond to that yet, sir.")
        
    return True    