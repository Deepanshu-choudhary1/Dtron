from agents.llm_agent import ask_llm

def confidence_score(answer):
    prompt = f"""
Rate your confidence in the following answer from 0 to 100.
Respond with ONLY a number.

ANSWER:
{answer}
"""
    score = ask_llm(prompt)
    return "".join(c for c in score if c.isdigit()) or "50"
