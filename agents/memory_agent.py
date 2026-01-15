import json
import os

MEMORY_FILE = "memory.json"

class MemoryAgent:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)

    def remember(self, role, content):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        memory.append({
            "role": role,
            "content": content
        })

        # keep memory small (last 20 entries)
        memory = memory[-20:]

        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)

    def recall(self):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    
    def get_recent_reflections(self, limit=5):
        with open("memory.json", "r") as f:
            memory = json.load(f)

        reflections = [
            m["content"]
            for m in memory
            if m["role"] == "reflection"
       ]

        return reflections[-limit:]

memory_agent = MemoryAgent()
