import speech_recognition as sr
import time

# ─────────────────────────────────────────
# 🎤 GLOBAL RECOGNIZER (INIT ONCE)
# ─────────────────────────────────────────
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.4


def listen(timeout=6, phrase_time_limit=10):
    """
    Listens safely for user speech.
    NEVER crashes the Dtron loop.
    Returns empty string on silence or failure.
    """

    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")

            # Small delay to avoid mic lock issues
            time.sleep(0.1)

            # Light ambient calibration (DO NOT overdo)
            recognizer.adjust_for_ambient_noise(source, duration=0.25)

            try:
                audio = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                # No speech detected
                return ""

        try:
            text = recognizer.recognize_google(audio)
            text = text.strip()
            if not text:
                return ""

            print(f"🗣️ You: {text}")
            return text.lower()

        except sr.UnknownValueError:
            # Speech not understandable
            return ""

        except sr.RequestError as e:
            # Google API issue
            print(f"❌ Speech API error: {e}")
            return ""

    except Exception as e:
        # Mic disconnected / OS error / permission issue
        print(f"⚠ Mic error: {e}")
        return ""
