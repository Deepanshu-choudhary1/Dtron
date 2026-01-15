from email.mime import text
import os
import subprocess
import webbrowser
import psutil

# Windows system apps registry
APP_COMMANDS = {
    "calculator": "calc",
    "notepad": "notepad",
    "paint": "mspaint",
    "command prompt": "cmd",
    "terminal": "cmd",
    "file explorer": "explorer",
    "explorer": "explorer",
    "control panel": "control",
    "task manager": "taskmgr",
    "settings": "ms-settings:",
    "camera": "microsoft.windows.camera:",
    "wordpad": "write",
    "powershell": "powershell",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": "msedge",
    "whatsapp": r"C:\Users\deepa\AppData\Local\WhatsApp\WhatsApp.exe",
}

PROCESS_NAMES = {
    "calculator": ["CalculatorApp.exe", "calc.exe"],
    "notepad": ["notepad.exe"],
    "paint": ["mspaint.exe"],
    "chrome": ["chrome.exe"],
    "edge": ["msedge.exe"],
    "powershell": ["powershell.exe"],
    "cmd": ["cmd.exe"],
}


def execute(action, data):
    text = data.lower()
    
    # ───── OPEN YOUTUBE ─────
    if "youtube" in text and action == "open_app":
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"


    # ───── OPEN APP ─────
    if action == "open_app":
        for app, cmd in APP_COMMANDS.items():
            if app in text:
                try:
                    subprocess.Popen(cmd, shell=True)
                    return f"Opening {app}"
                except Exception as e:
                    return f"Failed to open {app}: {e}"

        return "I could not find that application."

    # ───── CLOSE APP ─────
    if action == "close_app":
        for app, processes in PROCESS_NAMES.items():
            if app in text:
                closed = False
                for proc in psutil.process_iter(["name"]):
                    try:
                        if proc.info["name"] in processes:
                            proc.terminate()
                            closed = True
                    except:
                        pass
                return f"Closed {app}" if closed else f"{app} is not running"

        return "I could not find that application to close."

    # ───── WEB SEARCH ─────
    if action == "search":
        query = text.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}"

    return "Unknown action"
