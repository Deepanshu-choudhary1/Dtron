import json
from agents.llm_agent import ask_llm

def decide_tool(user_input):
    prompt = f"""
You are a tool-using AI agent.

Available tools:
- vision.read_screen
- executor.open_app
- web.search
- llm.talk

You may return ONE tool or a CHAIN of tools.

FORMAT (JSON ONLY):

Single:
{{
  "type": "single",
  "tool": "vision | executor | web | llm",
  "action": "...",
  "input": "..."
}}

Chain:
{{
  "type": "chain",
  "steps": [
    {{ "tool": "...", "action": "...", "input": "..." }},
    {{ "tool": "...", "action": "...", "input": "..." }}
  ]
}}

User request:
{user_input}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "type": "single",
            "tool": "llm",
            "action": "talk",
            "input": user_input
        }

