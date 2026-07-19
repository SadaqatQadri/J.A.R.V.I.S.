import webview
import gui_bridge
from voice import speak, listen, process_command
from news import get_news
from wake_word import wait_for_wake_word

def run_voice_loop():
    speak("JARVIS is now online, sir.")
    while not gui_bridge.stop_event.is_set():
        gui_bridge.update_status("idle", "Say 'Hey Jarvis' to wake me.")
        print(">>> Waiting for wake word.")
        wait_for_wake_word()

        gui_bridge.update_status("listening", "Yes, sir?")
        print(">>> Wake word detected, now listening.")
        command = listen()
        print(">>> Got command:", command)

        if command:
            keep_going = process_command(command)
            print(">>> Finished processing, keep_going=", keep_going)
            if not keep_going:
                gui_bridge.stop_event.set()

class API:
    def get_news_now(self):
        result = get_news()
        speak(result)
        gui_bridge.show_news(result)

    def stop_jarvis(self):
        speak("Shutting down, sir.")
        gui_bridge.stop_event.set()

if __name__ == "__main__":
    api = API()
    window = webview.create_window(
        "JARVIS",
        "hud.html",
        width=1200,
        height=800,
        background_color="#000000",
        js_api=api
    )
    gui_bridge.set_window(window)

    webview.start(run_voice_loop)