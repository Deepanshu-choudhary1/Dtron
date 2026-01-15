import threading
import time

from agents.listener_agent import listen
from agents.speaker_agent import speak
from agents.youtube_agent import play_youtube_video
from agents.executor_agent import execute
from agents.llm_agent import ask_llm
from agents.memory_agent import memory_agent
from agents.goal_agent import goal_agent
from agents.whatsapp_agent import send_whatsapp_message
from agents.whatsapp_parser import parse_whatsapp_command
from agents.vision_agent import read_screen
from agents.reasoning_agent import reason_over_text
from agents.nlp_agent import parse


# ─────────────────────────────────────────
# 🤖 Dtron CORE LOOP (SIGNAL-ONLY)
# ─────────────────────────────────────────
def Dtron_loop(bridge, stop_event: threading.Event):
    print("🟢 Dtron loop started")

    try:
        bridge.set_status.emit("ONLINE")
        bridge.set_message.emit("Hello, I am Dtron.")
        speak("Hello, I am Dtron.")

        while not stop_event.is_set():
            bridge.set_status.emit("LISTENING")

            command = listen()   # ⚠ listen() has NO timeout parameter
            if not command:
                continue

            command = command.lower().strip()
            memory_agent.remember("user", command)

            bridge.set_message.emit(f"You said: {command}")

            # ───── EXIT ─────
            if command in ["exit", "quit", "shutdown", "close Dtron"]:
                bridge.set_status.emit("OFFLINE")
                bridge.set_message.emit("Shutting down. Goodbye.")
                speak("Shutting down. Goodbye.")
                stop_event.set()
                return

            # ───── NLP ─────
            bridge.set_status.emit("THINKING")
            nlp_result = parse(command) or {}
            intent = nlp_result.get("intent", "llm")

            # ───── WHATSAPP ─────
            if intent == "whatsapp_message":
                parsed = parse_whatsapp_command(command)
                if not parsed:
                    bridge.set_message.emit("Could not understand WhatsApp message.")
                    speak("I could not understand the WhatsApp message.")
                    continue

                result = send_whatsapp_message(
                    parsed["contact"], parsed["message"]
                )
                bridge.set_status.emit("SPEAKING")
                bridge.set_message.emit(result)
                speak(result)
                continue

            # ───── YOUTUBE ─────
            if intent == "youtube_play":
                query = (
                    command.replace("play", "")
                    .replace("search", "")
                    .replace("on youtube", "")
                    .replace("youtube", "")
                    .strip()
                )

                speak(f"Playing {query} on YouTube")
                result = play_youtube_video(query) or "YouTube opened."

                bridge.set_status.emit("SPEAKING")
                bridge.set_message.emit(result)
                speak(result)
                continue

            # ───── OPEN / CLOSE APP ─────
            if intent in ("open_app", "close_app"):
                result = execute(intent, command)
                bridge.set_status.emit("SPEAKING")
                bridge.set_message.emit(result)
                speak(result)
                continue

            # ───── SEARCH ─────
            if intent == "search":
                execute("search", command)
                bridge.set_status.emit("SPEAKING")
                bridge.set_message.emit("Search completed.")
                speak("Search completed.")
                continue

            # ───── SCREEN / VISION ─────
            if intent == "read_screen":
                speak("Analyzing the screen")
                ocr_text = read_screen() or ""

                if not ocr_text.strip():
                    bridge.set_message.emit("No readable text on screen.")
                    speak("I could not read any text.")
                    continue

                reasoning = reason_over_text(ocr_text, command)
                bridge.set_status.emit("SPEAKING")
                bridge.set_message.emit(reasoning)
                speak(reasoning)
                continue

            # ───── AUTONOMOUS MODE ─────
            if "autonomous" in command:
                if "start" in command:
                    goal_agent.start(bridge)
                    bridge.set_message.emit("Autonomous mode activated.")
                    speak("Autonomous mode activated.")
                elif "stop" in command:
                    goal_agent.stop()
                    bridge.set_message.emit("Autonomous mode stopped.")
                    speak("Autonomous mode stopped.")
                continue

            # ───── LLM FALLBACK ─────
            bridge.set_status.emit("THINKING")
            bridge.set_message.emit("Thinking...")

            response = ask_llm(command)
            memory_agent.remember("llm", response)

            bridge.set_status.emit("SPEAKING")
            bridge.set_message.emit(response)
            speak(response)

    except Exception as e:
        print("❌ Dtron CRASH:", e)
        bridge.set_status.emit("ERROR")
        bridge.set_message.emit("System error occurred.")
        speak("A system error occurred.")
        print(f"❌ Dtron loop error: {e}")