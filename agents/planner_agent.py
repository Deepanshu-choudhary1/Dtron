
def plan(command):
    command = command.lower()

    # SCREEN / VISION
    if (
        "read screen" in command
        or "what is on my screen" in command
        or "read my screen" in command
    ):
        return {
            "type": "single",
            "agent": "vision",
            "task": "read_screen",
            "data": ""
        }
        
    # MULTI-STEP TASKS (examples)
    if "build" in command or "create" in command or "make" in command:
        return {
            "type": "multi",
            "steps": [
                "analyze the task",
                "design a solution",
                "generate code or explanation",
                "summarize the result"
            ],
            "goal": command
        }

    # SYSTEM
    if "open" in command:
        return {
            "type": "single",
            "agent": "executor",
            "task": "open_app",
            "data": command
        }

    if "search" in command:
        return {
            "type": "single",
            "agent": "executor",
            "task": "search",
            "data": command
        }

    # GOALS
    if "set scheduled goal" in command:
        return {
            "type": "goal",
            "data": command
        }

    if "start autonomous mode" in command:
        return {
            "type": "autonomy",
            "action": "start"
        }

    if "stop autonomous mode" in command:
        return {
            "type": "autonomy",
            "action": "stop"
        }

    # DEFAULT → LLM
    return {
        "type": "single",
        "agent": "llm",
        "task": "talk",
        "data": command
    }
