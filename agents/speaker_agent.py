import queue
import pyttsx3
import threading

speech_queue = queue.Queue()
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def _speech_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)

threading.Thread(target=_speech_worker, daemon=True).start()

def speak(text: str):
    if text:
        speech_queue.put(text)
