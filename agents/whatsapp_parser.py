from agents.llm_agent import ask_llm
import json

def parse_whatsapp_command(text):
    prompt = f"""
Extract WhatsApp contact name and message.

User command:
{text}

Respond in JSON ONLY.

FORMAT:
{{
  "contact": "name",
  "message": "text"
}}
"""
    try:
        response = ask_llm(prompt)
        return json.loads(response)
    except:
        return None
