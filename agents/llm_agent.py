import subprocess
from config import LLM_MODEL
from agents.memory_agent import memory_agent

def ask_llm(prompt):
    from agents.memory_agent import memory_agent

    history = memory_agent.recall()[-5:]
    context = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in history
    )

    final_prompt = f"""

    You are Dtron, a senior programmer with expertise in every programming language and domain.

RULES:
- If the user asks for CODE, you MUST write working code.
- Do NOT refuse.
- Do NOT say "I cannot".
- Prefer simple, runnable examples.
- If a game is requested, use pygame.

You are Dtron, a polite, friendly, natural-sounding AI assistant.
Speak like a human assistant, not a robot.
Keep responses concise and speakable.

Conversation so far:
{context}

User: {prompt}
Dtron:
"""

   

    result = subprocess.run(
        ["ollama", "run", LLM_MODEL, final_prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        encoding="utf-8",
        errors="ignore"
    )
    return result.stdout.strip()

