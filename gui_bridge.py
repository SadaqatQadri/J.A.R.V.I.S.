import json
import threading

window = None
stop_event = threading.Event()

def set_window(w):
    global window
    window = w

def update_status(state, text=""):
    if window:
        window.evaluate_js(f"setState({json.dumps(state)}, {json.dumps(text)})")

def show_news(text):
    if window:
        window.evaluate_js(f"renderNews({json.dumps(text)})")
        