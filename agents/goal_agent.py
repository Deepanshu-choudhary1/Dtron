import threading
import time
from agents.llm_agent import ask_llm
from agents.memory_agent import memory_agent

class GoalAgent:
    def __init__(self):
        self.goals = []
        self.running = False
        self.thread = None

    def add_goal(self, goal, interval=15):
        self.goals.append({
            "goal": goal,
            "interval": interval,
            "last_run": 0,
            "status": "active"
        })
        memory_agent.remember("goal", f"Scheduled goal: {goal}")
        

    def start(self, gui):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(
            target=self._run,
            args=(gui,),
            daemon=True
        )
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self, gui):
        gui.write("🧠 Autonomous Goal Agent started")

        while self.running:
            now = time.time()

        for g in self.goals:
            if g["status"] != "active":
                continue

            if now - g["last_run"] < g["interval"]:
                continue

            prompt = f"""
You are an autonomous agent.

Long-term goal:
{g['goal']}

Decide ONE small next step.
Do NOT complete the whole goal.
"""

            result = ask_llm(prompt)
            g["last_run"] = now

            memory_agent.remember("autonomy", result)
            gui.write(f"⏰ Goal step ({g['goal']}):")
            gui.write(result)

        time.sleep(2)


goal_agent = GoalAgent()
