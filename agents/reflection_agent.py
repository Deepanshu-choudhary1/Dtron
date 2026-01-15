from agents.llm_agent import ask_llm

def reflect(answer, critique):
    prompt = f"""
You are a self-improving AI.

ORIGINAL ANSWER:
{answer}

CRITIQUE:
{critique}

TASK:
- Reflect on the critique
- Extract 1 lesson to improve future answers
- Be concise
"""

    return ask_llm(prompt)
