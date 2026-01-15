from agents.llm_agent import ask_llm

def critique(original_answer, user_question):
    prompt = f"""
You are a critic AI.

USER QUESTION:
{user_question}

AI ANSWER:
\"\"\"
{original_answer}
\"\"\"

TASK:
- Identify any errors or unclear parts.
- Suggest improvements briefly.
- If answer is good, say "Answer is satisfactory".
"""

    return ask_llm(prompt)
