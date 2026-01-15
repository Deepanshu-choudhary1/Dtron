from agents.llm_agent import ask_llm

def reason_over_text(ocr_text, user_intent):
    prompt = f"""
You are an AI assistant with vision input.

USER INTENT:
{user_intent}

TEXT SEEN ON SCREEN (OCR):
\"\"\"
{ocr_text}
\"\"\"

TASK:
- Use ONLY the OCR text.
- Do NOT say you cannot see the screen.
- Reason carefully and explain clearly.
"""

    return ask_llm(prompt)
