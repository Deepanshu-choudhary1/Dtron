from math import e
import spacy

nlp = spacy.load("en_core_web_sm")

def parse(text):
    text = text.lower()
    entities = {}

    if any(k in text for k in ["exit", "quit", "shutdown", "close Dtron"]):
        intent = "exit"

    elif "whatsapp" in text and any(k in text for k in ["send", "message", "text"]):
        intent = "whatsapp_message"

    elif "youtube" in text and any(k in text for k in ["play", "search", "watch"]):
        intent = "youtube_play"

    elif any(k in text for k in ["open", "launch", "start"]):
        intent = "open_app"

    elif any(k in text for k in ["close", "terminate", "kill"]):
        intent = "close_app"

    elif any(k in text for k in ["search", "find", "lookup"]):
        intent = "search"

    elif any(k in text for k in ["screen", "see", "read"]):
        intent = "read_screen"

    else:
        intent = "chat"


    return {
        "intent": intent,
        "entities": entities,
        "text": text
    }
