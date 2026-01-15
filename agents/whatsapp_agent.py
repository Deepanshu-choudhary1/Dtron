import time
import pyautogui
from agents.executor_agent import execute

pyautogui.FAILSAFE = True

def send_whatsapp_message(contact_name, message):
    # 1. Open WhatsApp
    execute("open_app", "whatsapp")
    time.sleep(5)  # wait for app to load

    # 2. Click search box (top-left area)
    pyautogui.click(200, 120)
    time.sleep(0.5)

    # 3. Type contact name
    pyautogui.write(contact_name, interval=0.05)
    time.sleep(1)

    # 4. Open chat
    pyautogui.press("enter")
    time.sleep(1)

    # 5. Type message
    pyautogui.write(message, interval=0.05)
    time.sleep(0.5)

    # 6. Send
    pyautogui.press("enter")

    return f"Message sent to {contact_name} on WhatsApp"
